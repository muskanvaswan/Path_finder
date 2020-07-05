def output_image( maze, show_solution=True, show_explored=False):

    from PIL import Image, ImageDraw
    cell_size = 50
    cell_border = 2

    # Create a blank canvas
    img = Image.new(
        "RGBA",
        (maze.width * cell_size, maze.height * cell_size),
        "black"
    )
    draw = ImageDraw.Draw(img)

    maze.solution = maze.solution[1] if maze.solution is not None else None
    for i, row in enumerate(maze.walls):
        for j, col in enumerate(row):



            # Goal
            if (i, j) == maze.goal:
                fill = (0, 171, 28)

            # Solution
            elif maze.solution is not None and show_solution and (i, j) in maze.solution:
                fill = (220, 235, 113)

            # Walls
            elif not col:
                fill = (40, 40, 40)

            # Start
            elif (i, j) == maze.start:
                fill = (255, 0, 0)

            # Goal
            elif (i, j) == maze.goal:
                fill = (0, 171, 28)

            # Explored
            elif maze.solution is not None and show_explored and (i, j) in maze.explored:
                fill = (212, 97, 85)

            # Empty cell
            else:
                fill = (237, 240, 252)

            # Draw cell
            draw.rectangle(
                ([(j * cell_size + cell_border, i * cell_size + cell_border),
                  ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                fill=fill
            )

    img.save("maze.png")
