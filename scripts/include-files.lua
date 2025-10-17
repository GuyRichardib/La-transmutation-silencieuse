-- scripts/include-files.lua  (robuste + traçage)
local utils = require 'pandoc.utils'
local path  = require 'pandoc.path'

-- BASE_DIR déterminé de façon sûre et traçable
local function detect_base_dir()
  local base = '.'
  if PANDOC_STATE and PANDOC_STATE.input_files and #PANDOC_STATE.input_files > 0 then
    base = path.directory(PANDOC_STATE.input_files[1])
    if base == '' then base = '.' end
  end
  io.stderr:write(string.format('[include-files] BASE_DIR=%q\n', base))
  return base
end

local BASE_DIR = detect_base_dir()

local function candidates_for(p)
  p = tostring(p or ''):gsub('^%s+',''):gsub('%s+$','')
  p = p:gsub("^['\"]", ''):gsub("['\"]$", '')
  if p == '' then
    return {}
  end
  local c = {
    p,
    path.normalize(path.join({BASE_DIR, p})),
    path.normalize(path.join({BASE_DIR, 'manuscript', p})),
    path.normalize(path.join({'.', p})),
    path.normalize(path.join({'book', p})),
    path.normalize(path.join({'book', 'manuscript', p})),
  }
  return c
end

local function file_exists(fname)
  if not fname or fname == '' then return false end
  local fh = io.open(fname, 'r')
  if fh then fh:close(); return true end
  return false
end

local function resolve_to_existing(p)
  local tried, chosen = {}, nil
  for _, cand in ipairs(candidates_for(p)) do
    if cand and cand ~= '' then
      table.insert(tried, cand)
      if file_exists(cand) then chosen = cand; break end
    end
  end
  return chosen, tried
end

local function current_reader_format()
  local f = (PANDOC_STATE and PANDOC_STATE.input_format) or 'markdown'
  if not f:match('raw_tex') then
    f = f .. '+raw_tex'
  end
  return f
end

local function read_md_fragment(s)
  if not s or s == '' then
    return pandoc.List:new()
  end
  local fmt = current_reader_format()
  local opts = (PANDOC_STATE and PANDOC_STATE.reader_options) or nil
  return pandoc.read(s, fmt, opts).blocks
end

local function read_blocks_from_file(include_path)
  if type(include_path) ~= 'string' or include_path == '' then
    io.stderr:write('[include-files] include_path invalide: '..tostring(include_path)..'\n')
    os.exit(1)
  end
  local resolved, tried = resolve_to_existing(include_path)
  if not resolved then
    io.stderr:write(('[include-files] introuvable: %q\nTried:\n  - %s\n')
      :format(include_path, table.concat(tried, '\n  - ')))
    os.exit(1)
  end
  io.stderr:write(('[include-files] OK: %q -> %q\n'):format(include_path, resolved))
  local fh, err = io.open(resolved, 'r')
  if not fh then
    io.stderr:write('[include-files] io.open a échoué pour '..tostring(resolved)..' : '..tostring(err)..'\n')
    os.exit(1)
  end
  local content = fh:read('*a'); fh:close()
  return read_md_fragment(content)
end

local function expand_includes_in_text(txt)
  local out = pandoc.List:new()
  local any = false

  local i = 1
  for s, target, e in txt:gmatch('()@include%((.-)%)()') do
    local before = txt:sub(i, s - 1)
    if before and before:match('%S') then
      out:extend(read_md_fragment(before))
    end
    out:extend(read_blocks_from_file(target))
    any = true
    i = e
  end

  local tail = txt:sub(i)
  if tail and tail:match('%S') then
    out:extend(read_md_fragment(tail))
  end

  if any then return out else return nil end
end

local function expand_includes_in_text(txt)
  local out = pandoc.List:new()
  local any = false
  local reader_opts = (PANDOC_STATE and PANDOC_STATE.reader_options) or nil

  local i = 1
  for s, target, e in txt:gmatch('()@include%((.-)%)()') do
    local before = txt:sub(i, s - 1)
    if before and before:match('%S') then
      out:extend(pandoc.read(before, 'markdown', reader_opts).blocks)
    end
    out:extend(read_blocks_from_file(target))
    any = true
    i = e
  end

  local tail = txt:sub(i)
  if tail and tail:match('%S') then
    out:extend(pandoc.read(tail, 'markdown', reader_opts).blocks)
  end

  if any then return out else return nil end
end

local function maybe_include_from_block(blk)
  if blk.t == 'RawBlock' and blk.format == 'markdown' then
    return expand_includes_in_text(blk.text or '')
  end
  if blk.t == 'Para' or blk.t == 'Plain' then
    return expand_includes_in_text(utils.stringify(blk) or '')
  end
  return nil
end

return {
  {
    Para     = maybe_include_from_block,
    Plain    = maybe_include_from_block,
    RawBlock = maybe_include_from_block,
  }
}
