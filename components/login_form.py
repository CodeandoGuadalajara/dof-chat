"""Login form component for DOF Chat."""

import air


class LoginForm:
    """Component for user authentication form."""
    
    @staticmethod
    def create(action: str = "/login", title: str = "Login", error_message: str = None, **kwargs):
        """TODO: Login form implementation pending.
        
        This method is a placeholder. Authentication system is being 
        implemented by another team member.
        
        Returns:
            Placeholder div indicating TODO status
        """
        return air.Div(
            air.H2("🔐 Login System"),
            air.P("TODO: Authentication implementation in progress"),
            air.A("Continue to Demo", href="/demo", 
                  style="display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;"),
            style="text-align: center; padding: 2rem; border: 2px dashed #ccc; border-radius: 8px; margin: 2rem;"
        )