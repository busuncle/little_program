#include <stdio.h>
#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>


int main(int argc, char ** argv)
{
	lua_State * L = NULL;
	L = lua_open();

	luaL_openlibs(L);
	luaL_dofile(L, "test_c_call_lua.lua");

	lua_getglobal(L, "no_param_print");
	lua_pcall(L, 0, 0, 0);

	const char * pstr = "hello lua";
	lua_getglobal(L, "print_str");
	lua_pushstring(L, pstr);
	lua_pcall(L, 1, 0, 0);

	lua_getglobal(L, "add");
	// push params from left to right
	lua_pushinteger(L, 2);
	lua_pushinteger(L, 3);
	lua_pcall(L, 2, 1, 0); // 2 params, 1 return value
	// return value is on the top of stack
	printf("lua add function return value is %td \n", lua_tointeger(L, -1)); 
	lua_pop(L, 1);

	lua_close(L);
}
