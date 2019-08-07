class ARM_Attribute:
    """
    A class used to represent an attribute of an ARM Entity.

    Attributes
    ----------
    name : str
        The name of the attribute.
    data_type : str
        The data type of the attribute - defaulted to anyType.
    """

    def __init__(self, name, data_type="anyType"):
        """
        Args:
            name (str): The name of the attribute.
            data_type (str): Optional data type of the attribute.
                             Defaults to 'anyType' if no alternative provided.
        """
        self.name = name
        self.data_type = data_type

    def get_name(self):
        """Getter for name."""
        return self.name

    def get_data_type(self):
        """Getter for data type."""
        return self.data_type

    def __str__(self):
        """
        String representation of the attribute - its name and data type.
        e.g. 'Age (int)'
        """
        return "{} ({})".format(self.name, self.data_type)
