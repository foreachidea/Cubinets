#   []]] Cubinets, Copyright (C) 2026, Vytautas Rimkevicius
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

class Address:

    @staticmethod
    def indexToLabel(index):
        
        label = ""
        temp = index
        
        while temp > 0:
            temp -= 1
            label = chr(65 + (temp % 26)) + label
            temp = temp // 26
        
        return label

    @staticmethod
    def labelToIndex(label):

        # todo: check range/check if label
        if len(label) == 1:   # A..Z    
            
            return ord(label) - ord('A') + 1
        
        elif len(label) == 2:     # AA..ZZ

            return ((ord(label[0]) - ord('A') + 1) * 26 +
                    (ord(label[1]) - ord('A') + 1))
        
        else:
            # todo: raise more generic exception on wrong value - numeric, etc.
            # test what happens first
            raise ValueError(f"Column '{label}' exceeds ZZ")

            '''
            if (col < 0 || col > CellAddress::MAX_COLUMNS) {
                throw Base::ValueError("Out of range");
            }
            '''

    @staticmethod
    def extractLabel(address):

        label = ''.join(filter(str.isalpha, address)).upper()

        return label