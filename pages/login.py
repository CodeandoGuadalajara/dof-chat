"""Login page for DOF Chat."""

import air
from components.login_form import LoginForm


class LoginPage:
    """Page component for user authentication."""
    
    @staticmethod
    def render(error_message: str = None) -> air.Html:
        """Render the login page.
        
        TODO: Login functionality is being implemented by another team member.
        This is a placeholder page.
        
        Args:
            error_message: Optional error message to display
            
        Returns:
            Air Html component for the login page
        """
        return air.Html(
            air.Head(
                air.Title("DOF Chat - Login (TODO)"),
                air.Meta(charset="UTF-8"),
                air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            ),
            air.Body(
                LoginForm.create(),
                style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 2rem;"
            )
        )