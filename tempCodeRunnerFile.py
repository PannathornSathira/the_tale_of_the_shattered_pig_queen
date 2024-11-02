        g_state_manager.SetScreen(self.screen)
        
        # Define all states and set in StateMachine
        states = {
            "MAIN_MENU": BaseState(self.screen, self.font),
            "PLAY": PlayState(self.screen, self.font),
            "WORLD_MAP": MapSelectState(self.screen, self.font),
            "SHOP": ShopState(self.screen, self.font),
            "PAUSE": PauseState(self.screen, self.font),
        }
        g_state_manager.SetStates(states)
        
        # Start in Main Menu
        g_state_manager.Change("MAIN_MENU", {})