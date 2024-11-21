from numpy import ndarray, array

##########################################
# TO DO:
# DATASET
# # ADD PARAM DESC AND COMMENTS TO CLASS METHODS
# # FIX ERRORBARS
#
# UNIT
# # AUTOASSIGN NATURAL SCALE
#
# INTEGRATION BETWEEN UNIT AND DATASET
# # METHOD TO AUTO DIMENSIONALISE
# # METHOD TO AUTO NOT-DIMENSIONALISE?
##########################################


class Unit:
    def __init__(self, Data: int | float | ndarray, unit: str) -> None:
        self.__name__ = "Unit"
        self.value = Data
        self.unitStr = unit
        self.unitDict = self.makeUnitDict(self.unitStr)
        self.scaleDict = self.defineScales()
    
    def __repr__(self) -> str:
        return f"Unit({self.value} {self.unitStr})"
    
    def __str__(self) -> str:
        return f"{self.value} {self.unitStr}"
    
    def __add__(self, other: 'Unit') -> 'Unit':
        if isinstance(other, Unit):
            if self.unitDict == other.unitDict:
                return Unit(self.value + other.value, self.unitStr)
            else:
                return NotImplemented
        else:
            return NotImplemented

    def __sub__(self, other: 'Unit') -> 'Unit':
        if isinstance(other, Unit):
            if self.unitDict == other.unitDict:
                return Unit(self.value - other.value, self.unitStr)
            else:
                return NotImplemented
        else:
            return NotImplemented
        
    def __mul__(self, other: 'Unit') -> 'Unit' :
        result = self.unitDict.copy()
        if isinstance(other, Unit):
            for key, value in other.unitDict.items():
                if key in result:
                    if result[key] + value != 0:
                        result[key] += value
                    else:
                        result.pop(key)
                else:
                    result[key] = value
            return Unit(self.value * other.value, self.makeUnitStr(result))
        else:
            return Unit(self.value * other, self.unitStr)

    def __truediv__(self, other: 'Unit') -> 'Unit':
        result = self.unitDict.copy()
        if isinstance(other, Unit):
            for key, value in other.unitDict.items():
                if key in result:
                    if result[key] - value != 0:
                        result[key] -= value
                    else:
                        result.pop(key)
                else:
                    result[key] = value
            return Unit(self.value * other.value, self.makeUnitStr(result))
        else:
            return Unit(self.value * other, self.unitStr)
    
    def __pow__(self, other) -> 'Unit':
        if isinstance(other, int):
            result = self.unitDict.copy()
            for key, value in result.items():
                result[key] *= other
            return Unit(self.value**other, self.makeUnitStr(result))
        else:
            return NotImplemented

    def __rmul__(self, other: 'Unit') -> 'Unit':
        result = self.unitDict.copy()
        if isinstance(other, Unit):
            for key, value in other.unitDict.items():
                if key in result:
                    if result[key] + value != 0:
                        result[key] += value
                    else:
                        result.pop(key)
                else:
                    result[key] = value
            return Unit(self.value * other.value, self.makeUnitStr(result))
        else:
            return Unit(self.value * other, self.unitStr)

    def makeUnitDict(self, unitStr: str) -> dict[str, int]:
        unitDict: dict[str, int] = {}  # Format: {UnitName: Exponent}

        if len(unitStr.split("/")) > 1:
            posExp,  negExp = unitStr.split("/")
        else:
            posExp = unitStr
            negExp = ""

        if posExp != "":
            posExp = posExp.split("*")
        if negExp != "":
            negExp = negExp.split("*")

        if isinstance(posExp, list):
            for elem in posExp:
                if "^" in elem:
                    n = elem.split("^")
                    unitDict.update({n[0]: int(n[1])})
                else:
                    unitDict.update({elem: 1})
        if isinstance(negExp, list):
            for elem in negExp:
                if "^" in elem:
                    n = elem.split("^")
                    unitDict.update({n[0]: -int(n[1])})
                else:
                    unitDict.update({elem: -1})
        return unitDict.copy()

    def makeUnitStr(self, unitDict: dict[str, int]) -> str:
        unitStr = ""
        posExp = []
        negExp = []

        for key, value in unitDict.items():
            if value > 0:
                if value > 1:
                    posExp.append(key+"^"+str(value))
                else:
                    posExp.append(key)
            elif value < 0:
                if value < -1:
                    negExp.append(key+"^"+str(abs(value)))
                else:
                    negExp.append(key)

        if len(posExp) > 0 and len(negExp) > 0:
            return "*".join(posExp) + "/" + "*".join(negExp)
        elif len(posExp) > 0:
            return "*".join(posExp)
        elif len(negExp) < 0:
            return "1/" + "*".join(negExp)
        pass

class Dataset:
    def __init__(self, x_axis: list | ndarray, y_axis: list |ndarray, axesErrors: tuple[list, list] | tuple[ndarray, ndarray] = (None, None)) -> None:
        self.x_data = x_axis
        self.y_data = y_axis
        self.use_errors = False
        self.plot_options = {}
        
        ### Stupid way checking whether none, one or both indexes in axesErrors are None.
        if sum([True for x in axesErrors if type(x) != type(None)]) == 2:
            self.use_errors = True
            self.x_axis_error = axesErrors[0]
            self.y_axis_error = axesErrors[1]

    def configure_plots(self, **kwargs) -> None:
        """
        configure_plot creates a local dict of keyword arguments that later will be added to the plots and axes.
        """
        self.plot_options = kwargs

    def initialize_plot(self, ax):
        """
        initialize_plot adds sizes, text and a grid to the ax parameter utilising plot_options.
        """
        
        ### Opdate as needed with new kwargs and such
        labelsize = self.plot_options.get("labelsize", 10)
        ticksize = self.plot_options.get("ticksize", labelsize)
        titlesize = self.plot_options.get("titlesize", labelsize)

        title = self.plot_options.get("title", None)
        xlabel = self.plot_options.get("xlabel", None)
        ylabel = self.plot_options.get("ylabel", None)

        ax.grid(True)
        ax.set_title(title, fontsize = titlesize)
        ax.set_xlabel(xlabel, fontsize = labelsize)
        ax.set_ylabel(ylabel, fontsize = labelsize)
        ax.tick_params("both", labelsize = ticksize)

    def point_plot(self, ax = None) -> None:
        """
        point_plot() creates a point plot of x_data and y_data.\\
        Include ax parameter if you want to pair with other plots. 
        """
        from matplotlib.pyplot import subplots
        
        if ax == None:
            fig, ax = subplots(figsize = (7.5, 7.5))
        self.initialize_plot(ax)
        
        ax.plot(self.x_data, self.y_data,
                marker = self.plot_options.get("marker", "o"),
                color = self.plot_options.get("pointcolor", None),
                linestyle = "none"
                )
        
        if self.use_errors:
            ax.errorbar(self.x_data, self.y_data, 
                        yerr = self.y_axis_error,
                        fmt = "none",
                        ecolor = self.plot_options.get("pointcolor", None),
                        capsize = self.plot_options.get("capsize", 5)
                        )
            
            ax.errorbar(self.x_data, self.y_data,
                        xerr=self.y_axis_error,
                        fmt="none",
                        ecolor=self.plot_options.get("pointcolor", None),
                        capsize = self.plot_options.get("capsize", 5)
                        )


    def func_reg(self, regression_model: 'function', show_reg_info: bool = False, ax = None, info_ax = None) -> None:
        """
        func_reg() takes a function and makes a regression based on scipy's curve_fit.

        Parameters
        -------------------
        func : function / method
            Hello
        show_reg_info : bool
            World
        ax : ax or None
            Good
        info_ax: ax or None:
            Night
        """
        
        from matplotlib.pyplot import subplots, tight_layout
        from inspect import signature
        from scipy.optimize import curve_fit
        from numpy import linspace, sqrt, diag

        coeffs = list(signature(regression_model).parameters.keys())
        coeffs.pop(0)

        param, cov = curve_fit(regression_model, self.x_data, self.y_data)
        x_vals = linspace(min(self.x_data), max(self.x_data), 1000)

        if show_reg_info:
            if ax == None or info_ax == None:
                fig, (ax, info_ax) = subplots(1, 2, figsize=(15, 7.5))
            
            self.initialize_plot(ax)
            ax.plot(x_vals, regression_model(x_vals, *param), color = self.plot_options.get("linecolor", None))

            info_ax.axis("off")
            counter = 0
            for coeff, dev in zip(param, sqrt(diag(cov))):
                info_ax.text(0.5,1-0.15*counter,f"{coeffs[counter]} = {coeff}\n Error on {coeffs[counter]} = {dev}", fontsize = 15, ha='center', va='top')
                counter+=1
        else:
            if ax == None:
                fig, ax = subplots(figsize = (7.5,7.5))
            self.initialize_plot(ax)
            ax.plot(x_vals, regression_model(x_vals, *param), color = self.plot_options.get("linecolor", None))
        tight_layout()


def DataAnalyst(x_axis: list, y_axis: list, axesErrors: tuple[list, list] = (None, None)):
    return Dataset(x_axis, y_axis, axesErrors)
