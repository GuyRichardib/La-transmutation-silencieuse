-- scripts/include-files.lua
-- Filtre Pandoc pour remplacer les directives @include(path/to/file.md)
-- Version robuste : résout chemins, essaie plusieurs candidats, affiche logs clairs.

local utils = require 'pandoc.utils'
local path  = require 'pandoc.path'

local include_pat = '^%s*@include%((.-)%)%s*$'

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

local function file_exists(fname)
  local fh = io.open(fname, 'r')
  if fh then fh:close(); return true end
  return false
end

local function resolve_to_existing(p)
  local tried = {}
  for _, cand in ipairs(candidates_for(p)) do
    if cand and cand ~= '' then
      table.insert(tried, cand)
      if file_exists(cand) then
        return cand, tried
      end
    end
  end
  return nil, tried
end

local function read_blocks_from_file(include_path)
  local resolved, tried = resolve_to_existing(include_path)
  if not resolved then
    io.stderr:write(string.format("include-files.lua: cannot open %s\nTried: %s\n",
      tostring(include_path),
      table.concat(tried, " ; ")))
    os.exit(1) -- fail fast so CI signale l'emplacement exact manquant
  end

  -- lecture et parsing
  local fh, err = io.open(resolved, 'r')
  if not fh then
    io.stderr:write('include-files.lua: cannot open resolved file '..resolved..' : '..tostring(err)..'\n')
    os.exit(1)
  end
  local content = fh:read('*a'); fh:close()
  local reader_opts = nil
  if PANDOC_STATE and PANDOC_STATE.reader_options then reader_opts = PANDOC_STATE.reader_options end
  local parsed = pandoc.read(content, 'markdown', reader_opts)
  return parsed.blocks
end

local function maybe_include_from_block(blk)
  -- RawBlock in markdown form (e.g., a literal line `@include(...)`)
  if blk.t == 'RawBlock' and blk.format == 'markdown' then
    local inc = blk.text:match(include_pat)
    if inc then return read_blocks_from_file(inc) end
    return nil
  end

  -- For Para or Plain, stringify content and match
  if blk.t == 'Para' or blk.t == 'Plain' then
    local raw = utils.stringify(blk)
    if raw then
      local inc = raw:match(include_pat)
      if inc then return read_blocks_from_file(inc) end
    end
  end

  return nil
end

-- Export filter: handle Para, Plain and RawBlock
return {
  {
    Para     = maybe_include_from_block,
    Plain    = maybe_include_from_block,
    RawBlock = maybe_include_from_block,
  }
}
