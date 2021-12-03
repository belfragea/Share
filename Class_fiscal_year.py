import numpy as np, pandas as pd, math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from dataclasses import dataclass

@dataclass
class DM_Fiscal_Year:
    """Class for simulating a normal fiscal year"""
    name: str
    total_revenue: int = 600_000
    spring_season_sales: float = 0.25
    fall_season_sales: float = 0.35
    off_season_sales: float = 1 - spring_season_sales - fall_season_sales
    spring_season_days: int = 60
    fall_season_days: int = 60
    season_ramp_up_days: int = 21
    rng: object = np.random.default_rng(seed=42)
    
    def total_season_lenght(self) -> int:
        """Calculates the total season lenght of the fiscal year"""
        return self.spring_season_days + self.fall_season_days
    
    def avg_daily_revenue(self):
        duration = 365 - self.total_season_lenght()
        normal_revenue = self.total_revenue * self.off_season_sales
        return (normal_revenue/duration)
        
    def season_ramp_up(self, season_mean): #linear
        """calculate a ramp up/down week before/after the season"""
        
        daily_revenue = self.avg_daily_revenue()
        step = (season_mean - daily_revenue)/self.season_ramp_up_days
        up = []
        down = []
        ramp_up = daily_revenue
        ramp_down = daily_revenue
        
        #ramp up
        for i in range(self.season_ramp_up_days):
            ramp_up += step
            up.append(ramp_up + self.rng.integers(low=-40, high=40, size=1)[0])
            
        #ramp down
        down = up[::-1]
        
        return up, down
        
    def fallseason(self, plot: bool = False) -> list:
        """Calculates revenue per day during fall season. Optional: plotting"""
        fall_sales = self.total_revenue * self.fall_season_sales
        mean = fall_sales/self.fall_season_days 
        standard_deviation = mean / self.fall_season_days
        
        ramp_lists = self.season_ramp_up(mean)
        
        daily_sales = self.rng.normal(mean, standard_deviation, self.fall_season_days-(self.season_ramp_up_days*2)) #Assumes that the sales of the season is normally disitrubuted (rises against the mean) 
        
        fall_season_sales = []
        
        for i in range(self.season_ramp_up_days):
            fall_season_sales.append(ramp_lists[0][i])
        
        for i in range(len(daily_sales)):
            fall_season_sales.append(daily_sales[i])
            
        for i in range(self.season_ramp_up_days):
            fall_season_sales.append(ramp_lists[1][i])
        
        
        if plot:
            plt.plot(fall_season_sales)

        return fall_season_sales
    
    def springseason(self, plot: bool = False) -> list:
        """Calculates revenue per day during spring season. Optional: plotting"""
        spring_sales = self.total_revenue * self.spring_season_sales
        mean = spring_sales/self.spring_season_days 
        standard_deviation = mean / self.spring_season_days
        
        ramp_lists = self.season_ramp_up(mean)
        
        daily_sales = self.rng.normal(mean, standard_deviation, self.spring_season_days-(self.season_ramp_up_days*2)) #Assumes that the sales of the season is normally disitrubuted (rises against the mean) 
        
        spring_season_sales = []
        
        for i in range(self.season_ramp_up_days):
            spring_season_sales.append(ramp_lists[0][i])
        
        for i in range(len(daily_sales)):
            spring_season_sales.append(daily_sales[i])
            
        for i in range(self.season_ramp_up_days):
            spring_season_sales.append(ramp_lists[1][i])

        if plot:
            plt.plot(spring_season_sales)

        return spring_season_sales
    
    def offseasons(self) -> list:
        """Calculate revenue per day during off season."""
        daily_revenue = self.avg_daily_revenue()
        
        spring_start = 90 #90 days from jan to apr
        spring_end = spring_start + self.spring_season_days
        fall_start = 273
        fall_end = fall_start + self.fall_season_days
        
        first_off_season = []
        second_off_season = []
        third_off_season = []
        season_collection = []
        
        #First season
        for i in range(spring_start): 
            rev_day = daily_revenue + (self.rng.integers(low=-100, high=100, size=1))
            first_off_season.append(rev_day[0])
        
        #second season
        for i in range(fall_start - spring_end):
            rev_day = daily_revenue + (self.rng.integers(low=-100, high=100, size=1))
            second_off_season.append(rev_day[0])
            
        #Thrid season
        for i in range(365-fall_end):
            rev_day = daily_revenue + (self.rng.integers(low=-100, high=100, size=1))
            third_off_season.append(rev_day[0]) 
        
        season_collection.append(first_off_season)
        season_collection.append(second_off_season)
        season_collection.append(third_off_season)
        
        return season_collection 
            
    def daily_sales(self) -> list:
        """Calculates the daily sales of a complete fiscal year"""
        
        fiscal_year = []
        
        off_season = self.offseasons()
        spring_season = self.springseason()
        fall_season = self.fallseason()
        
        for i in range(len(off_season[0])):
            fiscal_year.append(off_season[0][i])
        
        for i in range(len(spring_season)):
            fiscal_year.append(spring_season[i])
        
        for i in range(len(off_season[1])):
            fiscal_year.append(off_season[1][i])
        
        for i in range(len(fall_season)):
            fiscal_year.append(fall_season[i])
        
        for i in range(len(off_season[2])):
            fiscal_year.append(off_season[2][i])
                
        return fiscal_year
    
    def sum_daily_sales(self):
        """helper method to sum the daily sales"""
        return sum(self.daily_sales())
    
    def descriptive_stats(self):
        """Helper method to return and print descriptive statistics about the simulation"""
        stats = pd.DataFrame(self.daily_sales()).describe()
        #print (stats)
        return stats

    def plot_self(self, to_plot: str):
        
        year = np.asarray(self.daily_sales())
        days = (np.arange(0, 365, 1))
        
        capacity1 = 1300
        capacity2 = 1800
        cap_increase = capacity2 - capacity1
        
        capacity_line1 = (np.full((365), capacity1))
        capacity_line2 = (np.full((365), capacity2))
        x = np.zeros(len(year))
        
        if to_plot == "fiscal_year":
            self.plot_fiscal_year(days, year)
            
        elif to_plot == "returns":
            self.plot_diminishing_returnL1()
            
        elif to_plot == "cap_1":
            self.plot_capacity1_fiscal_year(days, year, capacity_line1)
        
        elif to_plot == "cap_2":
            self.plot_capacity2_fiscal_year(days, year, capacity_line1, capacity_line2)
            
           
    def plot_fiscal_year(self, days, year):
        
        fig, (ax) = plt.subplots(1, 1, figsize=(18, 8))
        #FIG TITLE
        #fig.suptitle('Demand Tire Services', fontsize=24)
        
        #AX
        ax.plot(days, year, color='black', linestyle='solid', linewidth=1)
        ax.fill_between(days, year, where=year>days,color='lightsteelblue', interpolate=False, alpha=0.5)
        ax.yaxis.set_major_formatter('NOK {x:1.2f}')
        ax.set_title('Demand for tire services over simulated fiscal year', fontsize=22)
        ax.set_xlabel('Days', fontsize=18)
        ax.set_ylabel('Demand', fontsize=18, loc='center')
        ax.set_xticks(np.arange(0, 400, step=30))
        ax.set_ylim(0, np.amax(year) + 500)
        
        ax.grid(True)
        ax.set_xlim(0, 365)
        ax.yaxis.set_tick_params(which='major', labelcolor='black',
                         labelleft=True, labelright=False)
        
        plt.show()
        
    def plot_diminishing_returnL1(self): #IDEA = change output to tire shifts/day or something like that
        x = np.linspace(0,10,100) #Number of extra workers 
        y = -2*x**2+6*x+90 #output per seasonal worker
        
        fig_dim, (ax_dim, ax_acc) = plt.subplots(1, 2, figsize=(12, 5))
        
        #AX dim
        ax_dim.set_title('Diminishing return of seasonal workers')
        ax_dim.plot(x, y, color='red', linestyle='solid', linewidth=1)
        ax_dim.set_xlabel('# seasonal workers', fontsize=12)
        ax_dim.set_xticks(np.arange(0, 10, step=1))
        ax_dim.set_ylabel('marginal output', fontsize=12)
        ax_dim.grid(True)

        #AX acc
        u=0
        lst = []
        for x in range(0,12):
            z = -2*x**2+6*x+90
            u += z
            lst.append(u)
        
        ax_acc.set_title('Accumulated output of seasonal workers')
        ax_acc.plot(np.arange(0, 12 , 1), np.asarray(lst), color='red', linestyle='solid', linewidth=1)
        ax_acc.set_xlabel('# seasonal workers', fontsize=12)
        ax_acc.set_xticks(np.arange(0, 12, step=1))
        ax_acc.set_ylabel('accumulated output', fontsize=12)
        ax_acc.grid(True)
        
        plt.show()
        
    def plot_diminishing_returnL2(self):
        """Alternative diminishing return function"""
        #x = math.e**(-0.8*1) FUNCTION
        x = np.linspace(0,10,100) #Number of extra workers 
        k = 0.6 #Rate of the decaying return
        y = math.e**(-k*x)
        plt.plot(x, y)
        plt.show()
        
    def plot_capacity1_fiscal_year(self, days, year, capacity_line1):
        
        fig_cap, (ax_cap) = plt.subplots(1, 1, figsize=(18, 8))
        
        #Graph
        ax_cap.yaxis.set_major_formatter('NOK {x:1.2f}')
        ax_cap.set_title('Demand for tire services over simulated fiscal year', fontsize=22)
        ax_cap.set_xlabel('Days', fontsize=18)
        ax_cap.set_ylabel('Demand', fontsize=18, loc='center')
        ax_cap.set_xticks(np.arange(0, 400, step=30))
        ax_cap.set_ylim(0, np.amax(year) + 500)
        ax_cap.set_xlim(0, 365)
        ax_cap.grid(True)
        
        #Plotting
        ax_cap.plot(days, year, color='black', linestyle='solid', linewidth=1)
        ax_cap.plot(capacity_line1, color='black', linewidth=1, label='Capacity at t=1 \n'+r'$C = (A_{\alpha} + L_{\alpha} + LS_{1})*H_{1}$')
        ax_cap.fill_between(days, year, where=year>days,color='lightsteelblue', interpolate=False, alpha=0.5)
        ax_cap.fill_between(days, year, capacity_line1, where=year>capacity_line1, color='lightcoral', interpolate=False, alpha=1)
        ax_cap.fill_between(days, capacity_line1, year, where=year<capacity_line1,color='mistyrose', interpolate=False, alpha=0.5) 
        
        #LEGEND
        red_patch = mpatches.Patch(color='lightcoral', label='Lost potential revenue')
        yellow_patch = mpatches.Patch(color='mistyrose', label='Unutilized capacity', alpha=0.5)
        green_patch = mpatches.Patch(color='lightsteelblue', label='Collected revenue')
        color_legend = ax_cap.legend(handles=[red_patch, yellow_patch, green_patch], loc=2)
        line_legend = ax_cap.legend(loc=1)
        ax_cap.add_artist(color_legend)
        ax_cap.add_artist(line_legend)
        
        plt.show()
        
    
    def plot_capacity2_fiscal_year(self, days, year, capacity_line1, capacity_line2):
        
        fig_cap, (ax_cap) = plt.subplots(1, 1, figsize=(18, 8))
        
        #Graph
        ax_cap.yaxis.set_major_formatter('NOK {x:1.2f}')
        ax_cap.set_title('Demand for tire services over simulated fiscal year', fontsize=22)
        ax_cap.set_xlabel('Days', fontsize=18)
        ax_cap.set_ylabel('Demand', fontsize=18, loc='center')
        ax_cap.set_xticks(np.arange(0, 400, step=30))
        ax_cap.set_ylim(0, np.amax(year) + 500)
        ax_cap.set_xlim(0, 365)
        ax_cap.grid(True)
        
        #Plotting
        ax_cap.plot(days, year, color='black', linestyle='solid', linewidth=1)
        ax_cap.plot(capacity_line1, color='black', linewidth=1, label='Capacity at t=1 \n'+r'$C = (A_{\alpha} + L_{\alpha} + LS_{1})*H_{1}$')
        ax_cap.fill_between(days, year, where=year>days,color='lightsteelblue', interpolate=False, alpha=0.5)
        ax_cap.fill_between(days, capacity_line1, year, where=year<capacity_line1,color='mistyrose', interpolate=False, alpha=0.5)
        ax_cap.hlines(y=capacity_line2, xmin=90, xmax=150, linewidth=1, color='black', linestyle='dashed', label='Capacity at t=2 \n'+r'$C = (A_{\alpha} + L_{\alpha} + LS_{2})*H_{2}$')
        ax_cap.hlines(y=capacity_line2, xmin=270, xmax=330, linewidth=1, color='black', linestyle='dashed')
        ax_cap.fill_between(days, year, capacity_line2, where=year>capacity_line2, color='lightcoral', interpolate=False, alpha=1)
        
        #LEGEND
        red_patch = mpatches.Patch(color='lightcoral', label='Lost potential revenue')
        yellow_patch = mpatches.Patch(color='mistyrose', label='Unutilized capacity', alpha=0.5)
        green_patch = mpatches.Patch(color='lightsteelblue', label='Collected revenue')
        color_legend = ax_cap.legend(handles=[red_patch, yellow_patch, green_patch], loc=2)
        line_legend = ax_cap.legend(loc=1)
        ax_cap.add_artist(color_legend)
        ax_cap.add_artist(line_legend)
        
        plt.show()

