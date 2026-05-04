# Exam

## Q2. Same Size Respawn Feature
It will be better to test my codes without adding this feature to main loop cause i have issues with it.

## Q3. Screen Wrapping Feature
For this to work i will not remove the bouncing mechanism will just put it in comments. For his question need to make sceren wrapping everywhere. So horizontally and vertically i think it kind of works it's a bit slow but it works.

## Q4. Collision Detection Feature
To detect collisions between two squares I considered two approaches:

1. **Distance-based detection** 
2. **Rectangle-based detection** using pygame.Rect

Since my squares are already represented as rectangles (position + size), the most natural and reliable solution is to use **pygame.Rect**.

I create two rectangles using the position (x, y) and size of each square. Then I use the built-in method `colliderect()` which returns True if the rectangles overlap.

## Q5. Eating Feature
The goal is to make bigger squares eat smaller ones when they collide.
I reused the collision detection function from Exercise 4 to determine when two squares overlap.

The logic is:

Instead of removing the square from the list I chose to call its `reset()` method. This keeps the simulation stable and respects the requirement that eaten squares respawn.


## Q6. Eating++ Feature
The goal is the same as in exercise 5 the difference is it needs to get bigger by proportion

## Q7. Trails Feature


## Q8. Testing Speed Feature

## Q9. Animated Growth Feature

