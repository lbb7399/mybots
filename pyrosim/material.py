from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self,colorString):

        self.depth  = 3
        
        if colorString == 'blue':
        

            self.string1 = '<material name="Cyan">'

            self.string2 = '    <color rgba="0 1.0 1.0 1.0"/>'
            
        elif colorString == 'green':
        
            self.string1 = '<material name="Green">'

            self.string2 = '    <color rgba="0.4 1 0.4 1"/>'
            
        else:
            self.string1 = '<material name="Grey">'

            self.string2 = '    <color rgba="0.7 0.7 0.7 1.0"/>'
            

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
