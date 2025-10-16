local utils = require 'pandoc.utils'
local path  = require 'pandoc.path'

local include_pattern = '^%s*@include%((.-)%)%s*$'

-- Détermine le répertoire de base à partir du fichier d'entrée si possible
local function detect_base_dir()
  if PANDOC_STATE and PANDOC_STATE.input_files and #PANDOC_STATE.input_files > 0 then
    local base = path.directory(PANDOC_STATE.input_files[1])
    if base == '' then return '.' end
    return base
  end
  -- fallback : dossier 'book' si tu sais que c'est là que se trouvent les includes
  -- return 'book'
  return '.'
end

local BASE_DIR = detect_base_dir()

local function candidates_for(p)
  p = (p or ''):gsub('^%s+', ''):gsub('%s+$', '')          -- trim
  p = p:gsub("^['\"]", ""):gsub("['\"]$", "")             -- remove quotes if any
  local c = {}
  table.insert(c, p)                                      -- as provided (relative to cwd)
  table.insert(c, path.normalize(path.join({BASE_DIR, p}))) -- relative to base_dir (common)
  table.insert(c, path.normalize(path.join({BASE_DIR, 'manuscript', p}))) -- try book/manuscript/...
  table.insert(c, path.normalize(path.join({'.', p})))   -- repo-root relative
  return c
end

local function resolve(include_path)
  if path.is_absolute(include_path) then
    return include_path
  end
  return nil, tried
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
