import pygame

class ShopState:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.items = ["Health Potion", "Magic Scroll", "Gun Upgrade"]
        self.selected_item_index = 0

    def Exit(self):
        pass

    def Enter(self, params):
        pass

    def update(self, dt, events):
        # Handle player input for selecting items and purchasing
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_item_index = (self.selected_item_index + 1) % len(self.items)
                elif event.key == pygame.K_UP:
                    self.selected_item_index = (self.selected_item_index - 1) % len(self.items)
                elif event.key == pygame.K_RETURN:
                    print(f"Purchased {self.items[self.selected_item_index]}")  # Placeholder for purchase logic

    def render(self):
        # Fill the screen with a background color
        self.screen.fill((200, 200, 200))  # Light gray color

        # Render shop items
        for index, item in enumerate(self.items):
            color = (0, 255, 0) if index == self.selected_item_index else (0, 0, 0)
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, 150 + index * 50))
            self.screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.update()
