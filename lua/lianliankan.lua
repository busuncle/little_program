local test_maps = {
    -- a map is a 2-dimension table, use map[row][column] to fetch its element
    {
        {1, 2, 3, 4, 5},
        {2, 4, 3, 1, 1},
        {5, 2, 1, 5, 2},
        {2, 5, 3, 2, 3},
    },
    {
        {1, 2, 3, 4},
        {2, 1, 4, 3},
    },
    {
        {1, nil, 1, 2},
        {2, 3, nil, 3},
    },
    {
        {1, nil, 2},
        {4, 1, nil},
        {3, 3, nil},
        {4, 2, nil},
    },
}

local function connect_by_1(p1, p2, map)
    if p1.row == p2.row then
        local a, b = math.min(p1.column, p2.column)+1, math.max(p1.column, p2.column)-1
        for i = a, b do
            if map[p1.row][i] ~= nil then
                return false
            end
        end
        return true
    end
    if p1.column == p2.column then
        local a, b = math.min(p1.row, p2.row)+1, math.max(p1.row, p2.row)-1
        for i = a, b do
            if map[i][p1.column] ~= nil then
                return false
            end
        end
        return true
    end
    return false
end 

local function connect_by_2(p1, p2, map)
    -- try 2 dimensions from p1 to p2
    local step = (p2.row - p1.row) / math.abs(p2.row - p1.row)
    for i = p1.row+step, p2.row, step do
        if connect_by_1({row=i,column=p1.column}, p2, map) then
            return true
        end
    end

    step = (p2.column - p1.column) / math.abs(p2.column - p1.column)
    for i = p1.column+step, p2.column, step do
        if connect_by_1({row=p1.row,column=i}, p2, map) then
            return true
        end
    end
    return false
end

print("---------begin-------------")
print(connect_by_1({row=1,column=2}, {row=2,column=1}, test_maps[1]) == true) --false
print(connect_by_1({row=1,column=3}, {row=2,column=3}, test_maps[1]) == true) --true
print(connect_by_1({row=3,column=1}, {row=3,column=4}, test_maps[1]) == false) --false
print(connect_by_1({row=1,column=2}, {row=2,column=1}, test_maps[2]) == false) --false
print(connect_by_1({row=1,column=1}, {row=1,column=3}, test_maps[3]) == true) --true

print(connect_by_2({row=1,column=1}, {row=2,column=2}, test_maps[4]) == true) --true
print(connect_by_2({row=1,column=3}, {row=4,column=2}, test_maps[4]) == true) --true
print(connect_by_2({row=2,column=1}, {row=4,column=1}, test_maps[4]) == false) --false
print("---------end-------------")
