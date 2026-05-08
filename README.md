# Optimal Patrol Path Around Rectangular Machines

## 1. Mathematical Explanation

Each machine is represented as an **axis-aligned rectangle**.
The input gives two opposite corners of each rectangle:

```text
x1 y1 x2 y2
```

Since the rectangle is aligned with the x-axis and y-axis, we can find its four corner points as:

```text
(left, bottom)
(left, top)
(right, bottom)
(right, top)
```

where:

```text
left   = min(x1, x2)
right  = max(x1, x2)
bottom = min(y1, y2)
top    = max(y1, y2)
```

Therefore, instead of directly working with rectangles, we convert every rectangle into its **four corner points**.

For `N` rectangles, the total number of points becomes:

```text
M = 4N
```

So the original rectangle problem becomes:

> Find the shortest closed polygonal path that encloses all corner points of all rectangles.

---

### Why the Convex Hull Gives the Optimal Patrol Path ?

The robot must move along a closed path that encloses all rectangles.

A rectangle is a **convex shape**, meaning that if all four corners of a rectangle are inside or on a polygon, then the whole rectangle is also inside or on that polygon.

Therefore, enclosing all rectangle corners is enough to enclose all rectangles.

The shortest polygonal path enclosing a set of points is the **convex hull** of those points.

The convex hull is the smallest convex polygon that contains all given points. It can be imagined like stretching a rubber band around all the points. The rubber band forms the outer boundary, which is the convex hull.

So, for this problem:

```text
Minimum patrol path = perimeter of the convex hull of all rectangle corners
```

Any non-convex path enclosing the rectangles can be shortened by replacing inward bends with straight lines. Therefore, the optimal shortest path must be convex, and the smallest such convex boundary is the convex hull.

---

### Algorithm Used: Andrew’s Monotone Chain Algorithm

The implemented solution uses **Andrew’s Monotone Chain Algorithm** to compute the convex hull.

This algorithm is efficient and suitable for large input sizes such as:

```text
N ≤ 2 × 10^5
```

Since each rectangle gives four points:

```text
M = 4N
```

The algorithm works in three main steps:

1. Sort all points.
2. Build the lower hull.
3. Build the upper hull.
4. Combine both hulls to get the final convex hull.

---

## 2. Why Sorting the Points is Needed ?

The points are sorted by:

1. x-coordinate
2. y-coordinate, if x-coordinates are equal

In Python, this is done using:

```python
points = sorted(set(points))
```

Sorting is important because Andrew’s algorithm builds the hull from left to right and then from right to left.

After sorting:

* The **lower hull** is built by scanning points from left to right.
* The **upper hull** is built by scanning points from right to left.

Sorting also makes it easy to remove duplicate points using `set(points)`, which is useful because rectangles may touch and share corner points.

---

## 3. How Cross Products are Used to Build the Hull ?

While building the hull, the algorithm checks the direction of the turn made by the last two points in the current hull and the new point being added.

For three points:

```text
O = (Ox, Oy)
A = (Ax, Ay)
B = (Bx, By)
```

The cross product is:

```text
cross(O, A, B) = (Ax - Ox)(By - Oy) - (Ay - Oy)(Bx - Ox)
```

This value tells the orientation of the three points.

| Cross Product Value | Meaning                            |
| ------------------: | ---------------------------------- |
|               `> 0` | Counter-clockwise turn / left turn |
|               `< 0` | Clockwise turn / right turn        |
|               `= 0` | Collinear points                   |

In the code:

```python
while len(lower) >= 2 and cross(lower[-2], lower[-1], i) <= 0:
    lower.pop()
```

This means:

> If the last three points do not make a proper left turn, remove the middle point because it cannot be part of the outer convex boundary.

The same logic is used for both the lower hull and upper hull.

---

## 4. Building the Lower Hull

The lower hull represents the **bottom boundary** of the convex hull.

The algorithm processes the sorted points from left to right.

For each point `p`:

1. Check the last two points already in the lower hull.
2. Use the cross product to check whether adding `p` creates a valid left turn.
3. If it creates a clockwise turn or a straight-line middle point, remove the last point.
4. Add `p` to the lower hull.

Code:

```python
lower = []

for i in points:
    while len(lower) >= 2 and cross(lower[-2], lower[-1], i) <= 0:
        lower.pop()
    lower.append(i)
```

The condition:

```python
cross(lower[-2], lower[-1], i) <= 0
```

removes points that are not needed on the outer boundary.

---

## 5. Building the Upper Hull

The upper hull represents the **top boundary** of the convex hull.

It is built similarly to the lower hull, but the points are processed in reverse order, from right to left.

Code:

```python
upper = []

for i in reversed(points):
    while len(upper) >= 2 and cross(upper[-2], upper[-1], i) <= 0:
        upper.pop()
    upper.append(i)
```

After both hulls are created, the last point of each list is removed before combining them, because the starting and ending points are duplicated.

```python
return lower[:-1] + upper[:-1]
```

---

## 6. Mathematical Details

### Cross Product Formula

For three points:

```text
O = (Ox, Oy)
A = (Ax, Ay)
B = (Bx, By)
```

The orientation is calculated as:

```text
cross(O, A, B) = (Ax - Ox)(By - Oy) - (Ay - Oy)(Bx - Ox)
```

Interpretation:

```text
cross > 0  → left turn
cross < 0  → right turn
cross = 0  → collinear
```

This formula is used to decide whether a point should remain on the convex hull.

---

### Euclidean Distance Formula

The distance between two points:

```text
A = (x1, y1)
B = (x2, y2)
```

is:

```text
distance(A, B) = ((x2 - x1)² + (y2 - y1)²) ^ 0.5
```

This is used to calculate the length of each edge of the convex hull.

---

### Perimeter Formula

Assume the convex hull contains `k` points in order:

```text
P0, P1, P2, ..., Pk-1
```

The perimeter is the sum of distances between consecutive hull points, including the edge from the last point back to the first point.

In the code:

```python
for i in range(len(hull)-1):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1)]
        length += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    length += ((hull[0][0] - hull[-1][0]) ** 2 + (hull[0][1] - hull[-1][1]) ** 2) ** 0.5 
    return length
```

ensures that the final point connects back to the first point, forming a closed loop.

---

## 7. Time Complexity Analysis

Each rectangle gives 4 points.

So, for `N` rectangles:

```text
M = 4N
```

The main operations are:

| Step                   |   Complexity |
| ---------------------- | -----------: |
| Creating corner points |       `O(N)` |
| Sorting all points     | `O(M log M)` |
| Building lower hull    |       `O(M)` |
| Building upper hull    |       `O(M)` |
| Computing perimeter    |       `O(H)` |

Here, `H` is the number of points on the final convex hull.

Since:

```text
M = 4N
```

we get:

```text
O(M log M) = O(4N log 4N)
```

Ignoring constants:

```text
O(N log N)
```

Therefore, the overall time complexity is:

```text
O(N log N)
```

---

## 8. Output Precision

The problem requires the answer to have an absolute or relative error of at most:

```text
10^-6
```

This means the printed answer must be accurate up to around six decimal places.

The code prints the answer using:

```python
print(f"{len_hull:.8f}")
```
This prints 8 digits after the decimal point, which is more than enough for the required precision.

