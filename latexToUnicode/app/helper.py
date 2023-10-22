from .constants import *

class LatexParser():
    def __init__(self):
        self._BASIC_MATCH = BASIC_MATCHER
        self._CHAR_MATCH = CHAR_MATCHER
        self._SUPER = SUPER
        self._SUB = SUB
    
    @property
    def BASIC_MATCH(self):
        return self._BASIC_MATCH
    
    @property
    def CHAR_MATCH(self):
        return self._CHAR_MATCH
    
    @property
    def SUPER(self):
        return self._SUPER
    
    @property
    def SUB(self):
        return self._SUB
    
    def _clean_command(self, command:str) -> str:
        symbols = ['!', '#', '$', '%', '&', '*', '(', ')',
        '-', '+', '=', '/', '.', '>', '<', ',', ':', ';',
        '`', '~', '[', ']', '?', '|', '\'', '"', '\n']

        for symbol in symbols:
            command = command.split(symbol)[0]

        return command
    
    def _parse_text(self, s:str) -> dict:
        commands = ['\\'+self._clean_command(substring.split(' ')[0]) for substring in s.split('\\')[1:]]

        for command in commands:
            s = "__".join(s.split(command))
        
        return {
            "substrings": s.split("__"),
            "commands": commands
        }
    
    def _parse_sup_sub(self, command:'str'):
        if ('^' not in command) and ('_' not in command):
            return command, '', ''
        elif '_' not in command:
            return *command.split('^'), ''
        elif '^' not in command:
            return command.split('_')[0], '', command.split('_', 1)[-1]
        else:
            first, second = command.split('^')
            base, sup, sub = self._parse_sup_sub(first)
            if sub:
                return base, second, sub
            base, sup, sub = self._parse_sup_sub(second)
            return first, base, sub
        
    def _parse_command(self, command:str) -> str:
        base, sup, sub = self._parse_sup_sub(command)

        command = command.replace(base, '%')
        if sup:
            command = command.replace(sup, '?')
        if sub:
            command = command.replace(sub, '#')
        
        new_sup = ''.join([self.SUPER.get(char, char) for char in sup])
        new_sub = ''.join([self.SUB.get(char, char) for char in sub])

        if ('{' in base) and (('mathcal' in base) or ('mathbb' in base)):
            main, key = base.replace('}', '').split('{')
            new_base = self.CHAR_MATCH[main].get(key, base)
        
        elif '{' in base:
            new_base = base.split('{')
            new_base = ''.join([
                self.BASIC_MATCH.get(new_base[0], new_base[0]),
                '(',
                new_base[1].replace('{', '(').replace('}', ')')
            ])
            
        else:
            new_base = self.BASIC_MATCH.get(base, base)
        
        return command.replace('%', new_base).replace('?', new_sup).replace('#', new_sub).replace('_', '').replace('^', '')
    
    def _parse_substring(self, s:str) -> str:
        output = []
        for part in s.split(' '):
            if ('^' in part) or ('_' in part):
                sub = False
                sup = False
                parenthesis = 0
                out = ''
                for char in part:
                    if char == '_':
                        sub = True
                        continue
                    if char == '^':
                        sup = True
                        continue

                    if (char == '(') and (sup or sub):
                        parenthesis +=1
                    if char == ')':
                        parenthesis -=1

                    if sub:
                        out+=self.SUB.get(char, '_'+char)
                    if sup:
                        out+=self.SUPER.get(char, '^'+char)
                    
                    if (not sup) and (not sub):
                        out+=char
                        
                    if parenthesis:
                        continue

                    sup = False
                    sub = False
                output.append(out)
            else:
                output.append(part)
        return ' '.join(output)



    def parse(self, s:str) -> str:
        parse_dict = self._parse_text(s)
        substrings = [self._parse_substring(part) for part in parse_dict['substrings']]
        commands = parse_dict['commands']

        unicode = []
        for command in commands:
            unicode.append(self._parse_command(command))

        out = ''
        for k, v in zip(substrings, unicode+['']):
            out+=k+v

        return out