using System;

namespace SuperMarkoBrothers.Utils
{
    public static class MathUtils
    {
        public static float CalculateDistance(float x1, float y1, float x2, float y2)
        {
            float deltaX = x2 - x1;
            float deltaY = y2 - y1;
            return (float)Math.Sqrt(deltaX * deltaX + deltaY * deltaY);
        }

        public static float Lerp(float start, float end, float t)
        {
            return start + (end - start) * t;
        }
    }
}