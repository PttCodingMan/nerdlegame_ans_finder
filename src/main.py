from SingleLog.log import Logger

numbers = set('0123456789')
symbols = set('+-*/')


class Position:
    init_all = 1
    init_first = 2
    init_no_equal = 3
    init_no_symbols = 4

    def __init__(self, init_type):
        self.init_type = init_type

        if init_type == self.init_all:
            self.possible_symbols = numbers | symbols | set('=')
        elif init_type == self.init_first:
            self.possible_symbols = numbers - set('0')
        elif init_type == self.init_no_equal:
            self.possible_symbols = numbers | symbols
        elif init_type == self.init_no_symbols:
            self.possible_symbols = numbers


class Finder:
    def __init__(self):

        self.logger = Logger('Finder')
        self.positions = [
            Position(Position.init_first),

            Position(Position.init_no_equal),
            Position(Position.init_no_equal),
            Position(Position.init_no_equal),

            Position(Position.init_all),
            Position(Position.init_all),
            Position(Position.init_all),

            Position(Position.init_no_symbols),
        ]
        self._must_have = set()

    @classmethod
    def _last_number_length(cls, current_result: list[str]):
        if not current_result:
            return 0

        result = 0

        for n in reversed(current_result):
            if not n.isdigit():
                break
            result += 1

        return result

    def _count_func(self, current_result, level):
        # self.logger.info(level, current_result)

        current_position = self.positions[level]
        if len(current_position.possible_symbols) == 0:
            # print('return no possible symbols')
            return None

        # basic rule
        current_possible_symbols = current_position.possible_symbols.copy()
        if level == 0 or current_result[-1] in symbols:
            # The first position cannot be an operator symbol or zero
            # Any position after a symbol cannot be an operator symbol or zero
            # self.logger.info(level, current_result)
            current_possible_symbols -= symbols
            current_possible_symbols -= set('0')

        last_number_length = self._last_number_length(current_result)
        if last_number_length == 3:
            current_possible_symbols -= numbers

        if current_position.init_type == Position.init_all and current_result[-1] not in symbols:
            catch_error = False
            try:
                compute_result = float(eval("".join(current_result)))
                # print('->', level, type(compute_result), compute_result)
            except:
                catch_error = True
            if not catch_error:
                if compute_result.is_integer():
                    compute_result = str(int(compute_result))
                    if level + 1 + len(compute_result) == 8:

                        valid = True
                        for i, v in enumerate(compute_result):
                            # print(level + 1 + i, v, self.positions[level + 1 + i].possible_symbols)
                            if v not in self.positions[level + 1 + i].possible_symbols:
                                valid = False
                                break

                        if valid:
                            result = ''.join(current_result) + f'={compute_result}'
                            for m in self._must_have:
                                if m not in result:
                                    valid = False
                                    break

                            if valid:
                                return result
                            # elif '-' in current_result:
                            #     print('!!', self._must_have, current_result, compute_result)

        if level >= 6:
            # print('return type lv 6')
            return None

        # Tend to use different numbers
        rules = [
            (True,),
            (False,),
        ]

        for tend_to_use_different_numbers, in rules:
            # print(type(tend_to_use_different_numbers))
            for s in current_possible_symbols:
                if tend_to_use_different_numbers:
                    if s in current_result:
                        continue

                result = self._count_func(current_result + [s], level + 1)
                if result is None:
                    continue
                return result

        # print('return any possible')
        return None

    def _input(self):

        choice = [
            'p', 'b', 'g'
        ]

        while True:
            input_result = input('Need some help? Input result: ')

            self.logger.info('command', input_result)
            if len(input_result) != 8:
                continue

            valid = True
            for c in input_result:
                if c.lower() not in choice:
                    valid = False
                    break
            if not valid:
                continue

            break

        return [x.lower() for x in input_result]

    def count(self):

        # start_ans = ['6-41=-35', 'BPPPPBBP']
        start_ans = None

        while True:

            if start_ans is None:
                result = self._count_func([], 0)
            else:
                result = start_ans[0]
            self.logger.info('You can try', result)

            if start_ans is None:
                input_result = self._input()
            else:
                input_result = start_ans[1]
                start_ans = None

            for i, input_value in enumerate(input_result):
                # print(i, input_value, set(result[i]))
                match input_value.lower():
                    case 'b':
                        if result[i] not in self._must_have:
                            for ii in range(len(self.positions)):
                                self.positions[ii].possible_symbols -= set(result[i])
                        else:
                            self.positions[i].possible_symbols -= set(result[i])
                    case 'g':
                        self.positions[i].possible_symbols = set(result[i])
                    case 'p':
                        self.positions[i].possible_symbols -= set(result[i])
                        self._must_have.add(result[i])

        # self._input()


if __name__ == '__main__':
    finder = Finder()
    finder.count()
