import torch

import logging

logger = logging.getLogger(__name__)


class IntegrationTestFunction:
    """Wrapper class for test functions
    """

    domain = None  # Domain that is integrated over
    dim = None  # Expected input dimension of the function
    expected_result = None  # What the true integral solution is
    # Order of the function if applicable, can be used to infer expected convergence order
    order = None
    f = None  # Function to evaluate

    def __init__(self, expected_result, dim=1, domain=None):
        self.dim = dim
        self.expected_result = expected_result
        # Init domain to [-1,1]^dim if not passed
        if domain == None:
            self.domain = torch.tensor([[-1, 1]] * self.dim)
        else:
            self.domain = domain
        logging.debug("Initialized Test function with ")
        logging.debug(
            "dim="
            + str(self.dim)
            + "| domain="
            + str(self.domain)
            + "| expected_result="
            + str(expected_result)
        )

    def evaluate(integrator, integration_args):
        """Evaluates the passed integration functions with args

        Args:
            integrator (func): Integration function to call
            integration_args (list): arguments to pass to integrator

        Returns:
            float: integration result
        """
        return integrator(
            f=self.f, dim=self.dim, integration_domain=domain, *integration_args
        )


class Polynomial(IntegrationTestFunction):
    def __init__(self, expected_result=None, coeffs=[2], dim=1, domain=None):
        """N-dimensional , degree K poylnomial test functions

        Args:
            expected_result (torch.tensor): Expected results per dimension. Required to compute errors.
            coeffs (list, optional): Polynomial coefficients. Are the same for each dim. Defaults to [2].
            dim (int, optional): Polynomial dimensionality. Defaults to 1.
            domain (list, optional): Integration domain. Defaults to [-1.0, 1.0]^dim.
        """
        super().__init__(expected_result, dim, domain)
        self.coeffs = torch.tensor(coeffs)
        self.order = len(coeffs) - 1  # polynomial order is defined by the coeffs
        self.f = self._poly

    def _poly(self, x):
        # compute x^k
        exponentials = torch.pow(x, torch.arange(0, self.order + 1))

        print(exponentials)
        print(self.coeffs)
        # multiply by coefficients
        vals = torch.multiply(exponentials, self.coeffs)

        # sum all values for each dim
        return torch.sum(vals, dim=1)


class Exponential(IntegrationTestFunction):
    def __init__(self, expected_result=None, dim=1, domain=None):
        """Creates an n-dimensional exponential test function

        Args:
            expected_result (torch.tensor): Expected results per dimension. Required to compute errors.
            dim (int, optional): Input dimension. Defaults to 1.
            domain (list, optional): Integration domain. Defaults to [-1.0, 1.0]^dim.
        """
        super().__init__(expected_result, dim, domain)
        self.f = self._exp

    def _exp(self, x):
        # compute e^x
        return torch.exp(x)


class Sinusoid(IntegrationTestFunction):
    def __init__(self, expected_result=None, dim=1, domain=None):
        """Creates an n-dimensional exponential test function

        Args:
            expected_result (torch.tensor): Expected results per dimension. Required to compute errors.
            dim (int, optional): Input dimension. Defaults to 1.
            domain (list, optional): Integration domain. Defaults to [-1.0, 1.0]^dim.
        """
        super().__init__(expected_result, dim, domain)
        self.f = self._sinusoid

    def _sinusoid(self, x):
        return torch.sin(x)
