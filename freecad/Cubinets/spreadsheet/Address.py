# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

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