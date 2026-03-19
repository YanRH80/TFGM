--[[
  custom-blocks.lua — Universal block filter for academic publishing
  
  BLOCKS:
    ::: {.box title="..." wide="true" env="fpbox"}  → titled box
    ::: {.quote env="fpquote"}                       → styled blockquote  
  
  ATTRIBUTES:
    title  → heading text (box only)
    wide   → "true" spans both columns in twocolumn PDF
    env    → override LaTeX environment name (journal-specific)
    pos    → float position when wide (default: t!)
  
  EXTENDING: add an entry to the `handlers` table below.
  
  CONTRACT: each journal preamble must define at minimum:
    \begin{custombox}{Title}...\end{custombox}
    \begin{customquote}...\end{customquote}
  Journal-specific envs (fpbox, semergenbox...) are optional overrides.
]]

local function is_latex(fmt)
  return fmt:match("latex") or fmt:match("pdf")
end

local function is_docx(fmt)
  return fmt:match("docx")
end

local function raw_tex(s)
  return pandoc.RawBlock("latex", s)
end

local handlers = {}

-- ── .box {title="...", wide="true", env="fpbox"} ────────────
-- Attributes:
--   title  → box heading text
--   wide   → "true" to span both columns (PDF only)
--   env    → override LaTeX environment name (default: custombox)
--   pos    → float position when wide (default: t!)

handlers["box"] = function(el)
  local title   = el.attributes["title"] or ""
  local wide    = el.attributes["wide"] == "true"
  local env     = el.attributes["env"] or "custombox"
  local pos     = el.attributes["pos"] or "t!"
  local content = el.content

  if is_latex(FORMAT) then
    local out = pandoc.List({})
    if wide then
      out:insert(raw_tex("\\begin{figure*}[" .. pos .. "]"))
    end
    out:insert(raw_tex("\\begin{" .. env .. "}{" .. title .. "}"))
    out:extend(content)
    out:insert(raw_tex("\\end{" .. env .. "}"))
    if wide then
      out:insert(raw_tex("\\end{figure*}"))
    end
    return out

  elseif is_docx(FORMAT) then
    local title_para = pandoc.Para({pandoc.Strong({pandoc.Str(title)})})
    local blocks = pandoc.List({title_para})
    blocks:extend(content)
    local div = pandoc.Div(blocks)
    div.attributes["custom-style"] = "Block Text"
    return div

  else
    local title_para = pandoc.Para({pandoc.Strong({pandoc.Str(title)})})
    local blocks = pandoc.List({title_para})
    blocks:extend(content)
    return blocks
  end
end

-- ── .quote {env="fpquote"} ───────────────────────────────────
-- Attributes:
--   env → override LaTeX environment name (default: customquote)
handlers["quote"] = function(el)
  local env     = el.attributes["env"] or "customquote"
  local content = el.content

  if is_latex(FORMAT) then
    local out = pandoc.List({raw_tex("\\begin{" .. env .. "}")})
    out:extend(content)
    out:insert(raw_tex("\\end{" .. env .. "}"))
    return out

  elseif is_docx(FORMAT) then
    local italicized = pandoc.List({})
    for _, block in ipairs(content) do
      if block.t == "Para" then
        italicized:insert(pandoc.Para({pandoc.Emph(block.content)}))
      else
        italicized:insert(block)
      end
    end
    return {pandoc.BlockQuote(italicized)}

  else
    return {pandoc.BlockQuote(content)}
  end
end

-- NOTE: For wide figures, use Quarto's native attributes instead of Lua:
--   ![Caption](path.png){#fig-id fig-env="figure*" fig-pos="b!" width="100%"}

-- ═══════════════════════════════════════════════════════════════
function Div(el)
  for class, handler in pairs(handlers) do
    if el.classes:includes(class) then
      return handler(el)
    end
  end
  return nil
end
