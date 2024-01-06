from .english_test import test_router
from .interested_handler import interested_router
from .other_handlers import other_router
from .student_handlers import student_router, student_name_router
from .user_start import start_router

router_list = [
        start_router,
        student_router,
        student_name_router,
        interested_router,
        test_router,
        other_router
]
