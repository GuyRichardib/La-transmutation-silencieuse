-- Harmonise les tables pour les sorties PDF/EPUB/DOCX.
function Table(tbl)
  tbl.attr = tbl.attr or pandoc.Attr()
  if FORMAT:match('latex') then
    tbl.attr.classes:insert('longtable')
    return tbl
  elseif FORMAT:match('html') or FORMAT:match('epub') then
    tbl.attr.classes:insert('tbl')
    return tbl
  end
  return tbl
end