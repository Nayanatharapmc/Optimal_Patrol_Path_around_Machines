def cross(o, a, b):
    """Cross product of vectors OA and OB. A positive value indicates a counter-clockwise turn, 
    a negative value indicates a clockwise turn, and zero indicates a collinear point."""
    return ((a[0] - o[0]) * (b[1] - o[1])) - ((a[1] - o[1]) * (b[0] - o[0]))


def convex_hull(points):
    """Computes the convex hull of a set of points using the Monotone Chain algorithm."""
    if len(points) <= 1:
        return points

    # Building lower hull
    lower = []
    for i in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], i) <= 0:
            lower.pop()
        lower.append(i)

    # Building upper hull
    upper = []
    for i in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], i) <= 0:
            upper.pop()
        upper.append(i)

    return lower[:-1] + upper[:-1] # Removing the last point of each half because it's repeated at the beginning of the other half


def get_length(hull):
    """Calculates the perimeter of the convex hull."""
    if len(hull) < 2:
        return 0.0

    length = 0.0
    for i in range(len(hull)-1):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1)]
        length += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    length += ((hull[0][0] - hull[-1][0]) ** 2 + (hull[0][1] - hull[-1][1]) ** 2) ** 0.5 # Closing the hull by adding the distance between the last and the first point
    return length


def main():
    rect_count = int(input())
    points = set()  # Using a set to avoid duplicate points
    
    try:
        for _ in range(rect_count):
            x1, y1, x2, y2 = map(int, input().split())

            # Determining the corners of the rectangle
            left = min(x1, x2)    
            right = max(x1, x2)
            bottom = min(y1, y2)
            top = max(y1, y2)

            # Adding the corners of the rectangle to the set of points
            points.add((left, bottom))
            points.add((left, top))
            points.add((right, bottom))
            points.add((right, top))
    except Exception as e:
        print(f"Error reading input: {e}")
        return

    hull = convex_hull(sorted(points))
    len_hull = get_length(hull)
    print(f"{len_hull:.8f}")


if __name__ == "__main__":
    main()