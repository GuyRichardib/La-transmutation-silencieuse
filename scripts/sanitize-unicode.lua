local FORMAT_IS_LATEX = FORMAT:match("latex") ~= nil

local function sanitize(text)
  local s = text
  -- U+00A0 (non-breaking space) -> tie
  s = s:gsub("\194\160", "~")
  -- U+202F (narrow no-break space) -> fine space
  s = s:gsub("\226\128\175", "\\,{}")
  -- en dash / em dash -> TeX sequences
  s = s:gsub("–", "--")
  s = s:gsub("—", "---")
  return s
end

function Str(el)
  if FORMAT_IS_LATEX then
    return pandoc.Str(sanitize(el.text))
  end
  return nil
end
