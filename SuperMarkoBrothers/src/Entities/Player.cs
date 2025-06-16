using System;

namespace SuperMarkoBrothers.Entities
{
    public class Player
    {
        public Vector2 Position { get; set; }
        public int Health { get; set; }

        public Player(Vector2 startPosition)
        {
            Position = startPosition;
            Health = 100; // Default health
        }

        public void Move(float deltaX, float deltaY)
        {
            Position = new Vector2(Position.X + deltaX, Position.Y + deltaY);
        }

        public void Jump()
        {
            // Implement jump logic
        }

        public void Attack()
        {
            // Implement attack logic
        }
    }

    public struct Vector2
    {
        public float X { get; set; }
        public float Y { get; set; }

        public Vector2(float x, float y)
        {
            X = x;
            Y = y;
        }
    }
}