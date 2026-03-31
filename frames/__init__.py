from frames.dashboard import DashboardFrame
from frames.profile import ProfileFrame
from frames.vaccine import VaccineFrame
from frames.calendar_view import CalendarFrame
from frames.guide import GuideFrame
from frames.parasite import ParasiteFrame
from frames.medications import MedicationsFrame
from frames.appointments import AppointmentsFrame
from frames.nutrition import NutritionFrame
from frames.health import HealthFrame
from frames.expenses import ExpenseFrame
from frames.stats import StatsFrame
from frames.vets import VetFrame
from frames.gallery import GalleryFrame
from frames.settings import SettingsFrame

FRAME_MAP = {
    "dashboard": DashboardFrame, "profile": ProfileFrame, "vaccine": VaccineFrame,
    "calendar": CalendarFrame, "guide": GuideFrame, "parasite": ParasiteFrame,
    "medications": MedicationsFrame, "appointments": AppointmentsFrame,
    "nutrition": NutritionFrame, "health": HealthFrame, "expenses": ExpenseFrame,
    "stats": StatsFrame, "vets": VetFrame,
    "gallery": GalleryFrame, "settings": SettingsFrame,
}
