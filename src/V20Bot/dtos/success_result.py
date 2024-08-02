from enum import auto
from enum import Enum
from random import randint

import discord


class ResultStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    BOTCH = auto()
    WILLPOWER_NECESSARY = auto()


class ResultDetails:

    def __init__(self, player: discord.Member, **kwargs):
        self.Player: discord.Member = player
        self.Calculated: bool = False
        self.Rolls: list[int] = []
        self.Specialized: bool = False
        self.DicePool:int  = 0
        self.Successes: int = 0
        self.Botches: int = 0
        self.Explosions: int = 0
        self.Difficulty: int = 0
        self.Willpower: bool = False
        self.AutoSuccesses: int = 0
        self.Result: str = ""
        self.Target: discord.User = None
        self.__dict__.update(kwargs)

    def set_results(self, success_result: ResultStatus):

        if not self.Calculated:
            raise RuntimeError("Tried settings results before calculating them")

        match success_result:

            case ResultStatus.SUCCESS:
                self.Result = "Success!"
                self.ResultMessage = f"{self.Player.display_name} has succeeded with {self.Successes} successes!"
                if self.Explosions:
                    self.ResultMessage += f" ({self.Explosions} additional successes for specialty)"

            case ResultStatus.FAILURE:
                self.Result = "Failure!"
                self.ResultMessage = f"{self.Player.display_name} has failed the challenge!"

            case ResultStatus.BOTCH:
                self.Result = "BOTCHED"
                self.ResultMessage = f"{self.Player.display_name} botched the challenge!"

            case ResultStatus.WILLPOWER_NECESSARY:
                self.Result = "Success"
                self.ResultMessage = f"{self.Player.display_name} succeeded with 1 success due to willpower"

            case _:
                raise RuntimeError(f"Unhandled type of SuccessResults: {success_result}")

    def calculate_results(self):

        if self.Calculated:
            print("someone tried to reuse a roll calculation")
            return

        self.Rolls = [self.Difficulty for _ in range(self.AutoSuccesses)] +\
                     [randint(1, 10) for _ in range(max(0, self.DicePool - self.AutoSuccesses))]
        self.Rolls.sort()

        if self.Specialized:
            self.Explosions = len([result for result in self.Rolls if result == 10])
        self.Botches = len([result for result in self.Rolls if result == 1])
        self.Successes = len([result for result in self.Rolls if result >= self.Difficulty]) + self.Explosions

        willpower_needed = self.Botches > self.Successes and self.Willpower
        self.Successes = max(int(self.Willpower), self.Successes - self.Botches)

        self.Calculated = True

        if not self.Successes and self.Botches > self.Successes:
            self.set_results(ResultStatus.BOTCH)
            return

        if willpower_needed:
            self.set_results(ResultStatus.WILLPOWER_NECESSARY)
            return

        if self.Successes < 1:
            self.set_results(ResultStatus.FAILURE)
            return

        if self.Successes > 0:
            self.set_results(ResultStatus.SUCCESS)
            return

        response = f'The Bot was unable to determine the results.'
        response += f'\ndice_pool {self.DicePool}'
        response += f'\ndifficulty {self.Difficulty}'
        response += f'\nauto_successes {self.AutoSuccesses}'
        response += f'\nwillpower_used {self.Willpower}'
        response += f'\nrolls: ' + '  '.join([str(roll) for roll in self.Rolls])
        print(response)
