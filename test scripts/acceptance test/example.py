'''
Created on Nov 22, 2017

@author: tien.anh.nguyen
'''
from
class TestScenario1(TestScenarioBase):
    variable_2 = "abcd"
    def __init__(self):
        super(TestScenarioBase, self).__init__()
        
    def execute_precondition_steps(self):
        print self.variable_2
        super(TestScenario1,self).execute_precondition_steps()
        
    def execute_test_case(self):
        print 'go into execute_test_case_2'

if __name__ == '__main__':
    test_scenario = TestScenario1()
    test_scenario.execute_scenario()
        