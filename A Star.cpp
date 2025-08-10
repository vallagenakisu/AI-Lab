#include<bits/stdc++.h>
using namespace std;
int total_cost = 0;
struct Node {
    int r, c;
    int g; // cost so far
    int f; // g + h
    int pr, pc; // parent row, col
};

int heuristic(int r1, int c1, int r2, int c2) {
    return abs(r1 - r2) + abs(c1 - c2);
}

bool inside(int r, int c, int R, int C) {
    return r >= 0 && r < R && c >= 0 && c < C;
}

vector<pair<int,int>> a_star(vector<vector<int>> grid, pair<int,int> start, pair<int,int> goal) {
    int R = grid.size(), C = grid[0].size();
    vector<vector<int>> g(R, vector<int>(C, 1e9)); // 2D vector of costs
    vector<vector<pair<int,int>>> parent(R, vector<pair<int,int>>(C, {-1,-1})); // 2D vector of each cell parent
    vector<vector<bool>> visited(R, vector<bool>(C, false)); // 2D vector to track visit

    auto cmp = [](Node a, Node b){ return a.f > b.f; };
    priority_queue<Node, vector<Node>, decltype(cmp)> pq(cmp);

    g[start.first][start.second] = 0;
    pq.push({start.first, start.second, 0, heuristic(start.first, start.second, goal.first, goal.second), -1, -1});

    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};

    while (!pq.empty()) {
        Node cur = pq.top(); pq.pop();
        int r = cur.r, c = cur.c;

        if (visited[r][c]) continue;
        visited[r][c] = true;
        parent[r][c] = {cur.pr, cur.pc};

        //construct the path if goal is reached 
        if (r == goal.first && c == goal.second) {
            vector<pair<int,int>> path;
            for (int rr = r, cc = c; rr != -1 && cc != -1; tie(rr, cc) = parent[rr][cc]) {
                path.push_back({rr, cc});
            }
            total_cost = g[goal.first][goal.second];
            reverse(path.begin(), path.end());
            return path;
        }

        for (int i = 0; i < 4; i++) {
            int nr = r + dr[i], nc = c + dc[i];
            if (!inside(nr, nc, R, C) || grid[nr][nc] == 1) continue;

            int new_g = g[r][c] + 1;
            if (new_g < g[nr][nc]) {
                g[nr][nc] = new_g;
                int f  = heuristic(nr, nc, goal.first, goal.second);
                pq.push({nr, nc, new_g, f, r, c});
            }
        }
    }
    return {}; // no path
}

int main() {
    vector<vector<int>> grid = {
        {0,0,0,0,0},
        {0,1,1,1,0},
        {0,0,0,0,0},
        {0,1,1,0,0},
        {0,0,0,0,0}
    };

    pair<int,int> start = {0,0};
    pair<int,int> goal = {4,4};

    auto path = a_star(grid, start, goal);

    if (path.empty()) {
        cout << "No path found\n";
    } else {
        cout << "Path found:\n";
        for (auto [r,c] : path) {
            cout << "(" << r << "," << c << ") ";
            grid[r][c] = 2;
        }
    }
    cout << endl;
    cout << total_cost << endl;
}
