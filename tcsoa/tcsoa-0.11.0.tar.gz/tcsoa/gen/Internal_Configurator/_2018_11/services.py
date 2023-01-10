from __future__ import annotations

from tcsoa.gen.Internal.Configurator._2018_11.ConfiguratorManagement import ConfigurationRosterCoverage, ConfigurationRosterInput
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def getConfigurationRosterCoverage(cls, configurationRoster: ConfigurationRosterInput) -> ConfigurationRosterCoverage:
        """
        The Service operation expects a user to provide a set of configurations which are to be checked for validity
        and completeness. The service operation also returns a set of configurations which are unknown to the user.
        
        These configurations are passed to and returned by the service operation via a &lsquo;Roster Table&rsquo;. 
        
        A &lsquo;Roster Table&rsquo; is used to represent configurations. A &lsquo;Roster Table&rsquo; is capable of
        storing configurations. A configuration record in &lsquo;Roster Table&rsquo; is similar to saved variant rule.
        &lsquo;Roster Table&rsquo; consists of two parts,
        
        1.    Column Headers &ndash; A list of config expressions, one for each column in the table. A config
        expression is used to identify family name, family namespace, value and operator. Example: In the config
        Expression "[Teamcenter]A=A1", family name is A, namespace is "Teamcenter", operator is "=" and operand is "A1".
         
        2.    Rows &ndash; Rows store multiple row. A row contains a configuration, just like a Saved Variant Rule. The
        configuration is stored in a bit string, which means it can only contain &lsquo;0&rsquo; or &lsquo;1&rsquo;. 
        The total length of bit string is twice the number of columns present in &lsquo;Roster Table&rsquo;. Hence a
        string representing a cell has a size of 2.  Given string can only have either &lsquo;0&rsquo; or
        &lsquo;1&rsquo; the following strings can represent a cell. They are described below with their logical meaning
            a.    &lsquo;00&rsquo; &ndash; Both True and False conditions are possible for corresponding column header
        config Expression.
            b.    &lsquo;01&rsquo; &ndash; Only True condition is possible for corresponding column header config
        Expression.
            c.    &lsquo;10&rsquo; &ndash; Only False Condition is possible for corresponding column header config
        Expression.
            d.    &lsquo;11&rsquo; -  Not Defined
        
        A user input consisting of one/more configurations is passed to the service operation using &lsquo;Roster
        Table&rsquo;. These configurations are checked by the service operation for validity and completeness. An input
        &lsquo;Roster Table&rsquo; is said to be complete if the input &lsquo;Roster Table&rsquo; passed by user is
        able to represent all the possible combinations given no constraint is violated.
        
        User has ability to provide scope to the service operation while doing completeness check. This is done by
        passing a list of families. Only families present in the list are used by the service operation to compute the
        possible combinations and then evaluate whether the passed configurations via input &lsquo;Roster Table&rsquo;
        are able to cover each and every one of them.
        
        User also has an ability to provide &lsquo;explicit families&rsquo; to service operation. When a configuration
        from input &lsquo;Roster Table&rsquo; is checked for validity turns out to be &lsquo;invalid&rsquo; then
        service operation checks weather the reason for its invalidity is due to a family present in &lsquo;explicit
        families&rsquo;. If yes, then exception conditions on those family is checked, if we find an exception
        condition that meets the configuration input this implies the exception condition allows the configuration to
        be valid.
        
        Given all configurations passed via input &lsquo;Roster Table&rsquo; are valid, and they are able to represent
        all possible combinations then input is said to be complete. If they don&rsquo;t the configurations passed via
        input &lsquo;Roster Table&rsquo; are termed incomplete. Missing configurations are computed by service
        operation and returned via output &lsquo;Roster Table&rsquo;
        
        If some but not all configuration passed by user via &lsquo;Roster Table&rsquo; is found to be invalid, this
        means that the configuration wasn&rsquo;t able to satisfy constraints present in the system. User can specify
        severity of constraints which will participate in evaluating the configurations in input &lsquo;Roster
        Table&rsquo;. These invalid configurations are communicated back to the user and missing configurations are
        evaluated using valid configurations present in input &lsquo;Roster Table&rsquo;.
        
        If all the configurations passed to the service operation are invalid the service operation will return empty
        output &lsquo;Roster Table&rsquo;.
        
        Use Case 1: 
        A product context has 3 Boolean Families &lsquo;A&rsquo;, &lsquo;B&rsquo; and &lsquo;C&rsquo;.
        
        These 3 families can create a total of 8 configurations given there is no constraint in the system.
        
        A user can use &lsquo;getConfigurationRosterCoverage&rsquo; service operation to pass 3 configuration among the
        8 possible via input &lsquo;Roster Table&rsquo;. 
        
        In the current example all the 8 configurations are possible but the user only passed 3 of them in input. Hence
        the service operation provides verdict as &lsquo;valid&rsquo; for all the 3 input configurations. The remaining
        5 configurations are returned back to user via output &lsquo;Roster Table&rsquo;. Additionally service
        operation also returns a verdict of &lsquo;incomplete&rsquo; to user as he missed 5 possible configurations in
        input &lsquo;Roster Table&rsquo;.
        """
        return cls.execute_soa_method(
            method_name='getConfigurationRosterCoverage',
            library='Internal-Configurator',
            service_date='2018_11',
            service_name='ConfiguratorManagement',
            params={'configurationRoster': configurationRoster},
            response_cls=ConfigurationRosterCoverage,
        )
