from abc import ABC, abstractmethod
class AnalyticsUi(ABC):
    @abstractmethod
    def format_response_to_df(self, data):
        """
         implement your own logic in the concrete class that derive from here
        """
        pass
    @abstractmethod
    def analytics_tab(self):
        """
        implement your own logic in the concrete class that derive from here
        """
        pass
    
    @abstractmethod
    def create_conditional_bar_chart(self,df, category_col, value_col):
        """
        implement your own custom logic in derived classes.
        :return:
        """
        pass