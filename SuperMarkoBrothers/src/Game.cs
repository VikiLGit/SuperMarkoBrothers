using System;

namespace SuperMarkoBrothers
{
    public class Game
    {
        private bool isRunning;

        public Game()
        {
            isRunning = true;
        }

        public void Run()
        {
            Initialize();
            GameLoop();
        }

        private void Initialize()
        {
            // Initialization logic here
        }

        private void GameLoop()
        {
            while (isRunning)
            {
                Update();
                Render();
            }
        }

        private void Update()
        {
            // Update game state logic here
        }

        private void Render()
        {
            // Rendering logic here
        }

        public void Exit()
        {
            isRunning = false;
        }
    }
}