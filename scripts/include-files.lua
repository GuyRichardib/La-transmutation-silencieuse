local utils = require 'pandoc.utils'
local path = require 'pandoc.path'

local base_dir = '.'
if PANDOC_STATE and PANDOC_STATE.input_files and #PANDOC_STATE.input_files > 0 then
  base_dir = path.directory(PANDOC_STATE.input_files[1])
  if base_dir == '' then
    base_dir = '.'
  end
end

local function resolve_path(include_path)
  if path.is_absolute(include_path) then
    return include_path
  end
  return path.normalize(path.join({ base_dir, include_path }))
end

local function read_blocks(include_path)
  local filename = resolve_path(include_path)
  local fh, err = io.open(filename, 'r')
  if not fh then
    io.stderr:write('include-files.lua: cannot open ' .. filename .. ': ' .. (err or '') .. '\n')
    os.exit(1)
  end
  local contents = fh:read('*a')
  fh:close()
  local reader_options = nil
  if PANDOC_STATE then
    reader_options = PANDOC_STATE.reader_options
  end
  local parsed = pandoc.read(contents, 'markdown', reader_options)
  return parsed.blocks
end

local include_pattern = '^@include%((.-)%)$'

local function extract_include(blk)
  if blk.t == 'RawBlock' and blk.format == 'markdown' then
    return blk.text:match(include_pattern)
  end
  if blk.t == 'Para' or blk.t == 'Plain' then
    local raw = utils.stringify(blk)
    if raw then
      return raw:match(include_pattern)
    end
  end
  return nil
end

function Pandoc(doc)
  local out = pandoc.List()
  for _, blk in ipairs(doc.blocks) do
    local include_path = extract_include(blk)
    if include_path then
      out:extend(read_blocks(include_path))
    else
      out:insert(blk)
    end
  end
  return pandoc.Pandoc(out, doc.meta)
end
