-- Pandoc Lua filter ensuring NBSP/NNBSP survive serialization.
-- Emits raw LaTeX for spacing commands to avoid escaping when targeting XeLaTeX.
-- For other formats, the original Unicode characters are preserved.

local utf8 = require 'utf8'

local latex_map = {
  [' '] = '\nobreakspace',
  [' '] = '\nobreak\thinspace',
}

local function flush_buffer(result, buffer)
  if #buffer > 0 then
    result:insert(pandoc.Str(table.concat(buffer)))
    for i = #buffer, 1, -1 do buffer[i] = nil end
  end
end

local function sanitize_str(el)
  local text = el.text or ''
  if text == '' then
    return nil
  end
  if not text:find(' ', 1, true) and not text:find(' ', 1, true) then
    return nil
  end

  local result = pandoc.List:new()
  local buffer = {}
  local format = FORMAT or ''
  local is_latex = format:match('latex') or format:match('tex$') or format:match('beamer')

  for _, codepoint in utf8.codes(text) do
    local ch = utf8.char(codepoint)
    local replacement = latex_map[ch]
    if replacement then
      flush_buffer(result, buffer)
      if is_latex then
        result:insert(pandoc.RawInline('latex', replacement))
      else
        result:insert(pandoc.Str(ch))
      end
    else
      buffer[#buffer + 1] = ch
    end
  end
  flush_buffer(result, buffer)

  if result:length() == 1 and result[1].t == 'Str' and result[1].text == text then
    return nil
  end
  return result
end

return {
  { Str = sanitize_str },
}
