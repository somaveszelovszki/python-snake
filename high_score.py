import graphics
import pygame


class HighScore:
    def __init__(self, rank: int, name: str, score: int) -> None:
        self.rank = rank
        self.name = name
        self.score = score

    def __str__(self) -> str:
        return (
            f'{{ "rank": {self.rank}, "name": "{self.name}", "score": {self.score} }}'
        )

    def __repr__(self) -> str:
        return str(self)

    def draw(self, surface: pygame.Surface):
        text = pygame.font.Font(None, 36).render(
            f"{self.rank}. {self.name}: {self.score}", True, graphics.Color.WHITE.value
        )

        surface.blit(
            text,
            graphics.get_centered_offset(surface.get_size(), text.get_size()),
        )


class HighScoreTopBar:
    def __init__(self) -> None:
        self._back_navigation_requested = False

    def back_navigation_requested(self) -> bool:
        return self._back_navigation_requested

    def draw(self, surface: pygame.Surface):
        text = pygame.font.Font(None, 36).render(
            f"High scores", True, graphics.Color.WHITE.value
        )

        surface.blit(
            text, graphics.get_centered_offset(surface.get_size(), text.get_size())
        )


class HighScoreTable:
    def __init__(self, high_scores: list, row_size: tuple) -> None:
        self._high_scores = high_scores
        self._row_size = row_size
        self._running = True

    def is_running(self) -> bool:
        return self._running

    def get_size(self) -> tuple:
        return (self._row_size[0], self._row_size[1] * len(self._high_scores))

    def draw(self, surface: pygame.Surface):
        for i, high_score in enumerate(self._high_scores):
            offset = (
                (surface.get_width() - self._row_size[0]) // 2,
                (surface.get_height() - self._row_size[1] * len(self._high_scores)) // 2
                + i * self._row_size[1],
            )

            high_score.draw(surface.subsurface(offset, self._row_size))


class HighScoreWindow:
    def __init__(self, high_scores: list) -> None:
        self._top_bar = HighScoreTopBar()
        self._table = HighScoreTable(high_scores, row_size=(400, 50))

    def is_running(self) -> bool:
        return not self._top_bar.back_navigation_requested()

    def draw(self, surface: pygame.Surface):
        surface.fill(graphics.Color.BLACK.value)

        top_bar_height = 50

        content_size = (surface.get_width(), top_bar_height + self._table.get_size()[1])
        content_surface = surface.subsurface(
            (
                graphics.get_centered_offset(surface.get_size(), content_size),
                content_size,
            )
        )

        top_bar_surface = content_surface.subsurface(
            (0, 0, content_surface.get_width(), top_bar_height)
        )

        table_surface = content_surface.subsurface(
            (
                0,
                top_bar_height,
                content_surface.get_width(),
                content_surface.get_height() - top_bar_height,
            )
        )

        self._top_bar.draw(top_bar_surface)
        self._table.draw(table_surface)
