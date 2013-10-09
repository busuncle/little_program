-- first line, create this table, name it what you want, _M is good
local this_is_a_module = {}

this_is_a_module.sub_module_a = {}
function this_is_a_module.function_a()
    return "this is a function of the module"
end

-- the last line, return this table
return this_is_a_module


--[[
--  usage: 
--  local m = require "easiest_way_create_module"
--  print(m.function_a())
--]]
