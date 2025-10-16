local utils = require 'pandoc.utils'
local path  = require 'pandoc.path'

local include_pattern = '^%s*@include%((.-)%)%s*$'

local base_dir = '.'
if PANDOC_STATE and PANDOC_STATE.input_files and #PANDOC_STATE.input_files > 0 then
  base_dir = path.directory(PANDOC_STATE.input_files[1])
  if base_dir == '' then
    base_dir = '.'
  end
end

local function resolve(include_path)
  if path.is_absolute(include_path) then
    return include_path
  end
  return path.normalize(path.join({ base_dir, include_path }))
end

local function read_blocks(include_path)
  local filename = resolve(include_path)
  local fh, err = io.open(filename, 'r')
  if not fh then
    io.stderr:write('include-files.lua: cannot open ' .. include_path .. ': ' .. (err or '') .. '\n')
    os.exit(1)
  end
  local contents = fh:read('*a')
  fh:close()

  local reader_options = nil
  if PANDOC_STATE then
    reader_options = PANDOC_STATE.reader_options
  end

  return pandoc.read(contents, 'markdown', reader_options).blocks
end

local function include_from_block(blk)
  if blk.t == 'RawBlock' and blk.format == 'markdown' then
    local include_path = blk.text:match(include_pattern)
    if include_path then
      return read_blocks(include_path)
    end
  end

  if blk.t == 'Para' or blk.t == 'Plain' then
    local raw = utils.stringify(blk)
    if raw then
      local include_path = raw:match(include_pattern)
      if include_path then
        return read_blocks(include_path)
      end
    end
  end

  return nil
end

return {
  {
    Para     = include_from_block,
    Plain    = include_from_block,
    RawBlock = include_from_block,
  }
}
