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
  return path.normalize(path.join({base_dir, include_path}))
end

local function read_file(filename)
  local fh, err = io.open(filename, 'r')
  if not fh then
    io.stderr:write('include-files.lua: cannot open ' .. filename .. ': ' .. (err or '') .. '\n')
    os.exit(1)
  end
  local contents = fh:read('*a')
  fh:close()
  return contents
end

local function include_file(include_path)
  local filename = resolve_path(include_path)
  local contents = read_file(filename)
  local reader_format = 'markdown'
  local reader_options = nil
  if PANDOC_STATE then
    reader_options = PANDOC_STATE.reader_options
  end
  local parsed = pandoc.read(contents, reader_format, reader_options)
  return parsed.blocks
end

local include_pattern = '^@include%(([^)]+)%)$'

local function handle_block(el)
  local raw = utils.stringify(el)
  local include_path = raw:match(include_pattern)
  if not include_path then
    return nil
  end
  local blocks = include_file(include_path)
  return blocks
end

function Para(el)
  local blocks = handle_block(el)
  if blocks then
    return blocks
  end
end

function Plain(el)
  local blocks = handle_block(el)
  if blocks then
    return blocks
  end
end

function RawBlock(el)
  if el.format ~= 'markdown' then
    return nil
  end
  local include_path = el.text:match(include_pattern)
  if not include_path then
    return nil
  end
  local blocks = include_file(include_path)
  return blocks
end

return {
  { Para = Para, Plain = Plain, RawBlock = RawBlock }
}
