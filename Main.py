from Game import Game
from Board import Board

def main():
    game = Game()
    game.begins()

    i_positions = [input(), input(), input()]
    game.check_position(i_positions)
    i_positions = game.check_position(i_positions)
    game.set_state(i_positions)
    #Board.print_board(game.board)

    game.goal_state_info()
    g_positions = [input(), input(), input()]
    game.check_position(g_positions)
    g_positions = game.check_position(g_positions)
    game.set_goal_state(g_positions)
    Board.print_board(game.board)

if __name__ == "__main__":
    main()