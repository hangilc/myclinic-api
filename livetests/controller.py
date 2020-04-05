import asyncio
from typing import Dict
import aiohttp
from threading import Thread
import signal
import kanjidate
import practicelogbody
from model import *


class ControllerFactory:
    def __init__(self, url, enable_keyboard_interrupt=True):
        self.url = url
        self.loop = asyncio.new_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.t = None
        if enable_keyboard_interrupt:
            signal.signal(signal.SIGINT, signal.SIG_DFL)
        self._start()

    def _start(self):
        def thread_fun():
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        t = Thread(target=thread_fun)
        t.setDaemon(True)
        self.t = t
        t.start()

    def create_reception_controller(self):
        return ReceptionController(self.loop, self.session, self.url + "/remote/reception/client")

    def create_practice_log_listener(self):
        return PracticeLogListener(self.loop, self.session, self.url + "/practice-log")


class Listener:
    def __init__(self, loop, session, url):
        self.loop = loop
        self.session = session
        self.url = url
        self.lookahead = []
        self.queue = asyncio.Queue(loop=self.loop)
        self.ws = None
        self._connect(url)
        self._start_queue()

    def _connect(self, url):
        async def f():
            return await self.session.ws_connect(url)

        fut = asyncio.run_coroutine_threadsafe(f(), self.loop)
        self.ws = fut.result()

    def _start_queue(self):
        async def f():
            while True:
                msg = await self.ws.receive()
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self.queue.put(msg.json())
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break

        asyncio.run_coroutine_threadsafe(f(), self.loop)

    def clear_lookahead(self):
        self.lookahead = []

    def pop(self):
        async def f():
            return await self.queue.get()

        msg = asyncio.run_coroutine_threadsafe(self.queue.get(), self.loop).result()
        print(msg)
        return msg

    def pop_test(self, test):
        for cache in self.lookahead:
            if test(cache):
                self.lookahead.remove(cache)
                return cache
        while True:
            msg = self.pop()
            if test(msg):
                return msg
            else:
                self.lookahead.append(msg)

    def pop_equal(self, obj):
        return self.pop_test(lambda m: m == obj)


class PracticeLogListener(Listener):
    def __init__(self, loop, session, url):
        super().__init__(loop, session, url)

    def pop(self):
        msg = super().pop()
        plog = PracticeLog.from_dict(msg)
        body = practicelogbody.parse_body(plog)
        return plog, body


class Controller(Listener):
    def __init__(self, loop, session, url):
        super().__init__(loop, session, url)
        self.query_id = 1

    def _emit(self, message):
        asyncio.run_coroutine_threadsafe(self.ws.send_json(message), self.loop)

    def click(self, selector):
        self._emit({"command": "click", "selector": selector})

    def set_text(self, selector, text):
        self._emit({"command": "set-text", "selector": selector, "text": text})

    def get_text(self, selector):
        qid = self.query_id
        self.query_id += 1
        self._emit({"command": "get-text", "selector": selector, "id": qid})

        def test(msg):
            return msg["event"] == "get-text-result" and msg["id"] == qid
        reply = self.pop_test(test)
        return reply["result"]

    def wait_for_window_created(self, name):
        self.pop_equal({"event": "window-created", "class-name": name})

    def wait_for_window_closed(self, name):
        self.pop_equal({"event": "window-closed", "class-name": name})


class ReceptionController(Controller):
    def __init__(self, loop, session, url):
        super().__init__(loop, session, url)

    def open_new_patient_window(self):
        self.click("MainPane/NewPatientButton")
        self.wait_for_window_created("EnterPatientStage")
        return NewPatientWindow(self)


def sqldate_to_date(sqldate) -> datetime.date:
    if isinstance(sqldate, str):
        return datetime.datetime.strptime(sqldate, "%Y-%m-%d").date()
    elif isinstance(sqldate, datetime.date):
        return sqldate
    else:
        raise Exception("Cannot convert to date")


def sex_to_kanji(sex: str) -> str:
    if sex == "M":
        return "男"
    elif sex == "F":
        return "女"
    else:
        raise Exception("Unknown sex: " + sex)


class DateInputFormValues:
    def __init__(self):
        self.gengou = None
        self.nen = None
        self.month = None
        self.day = None

    def as_date(self) -> datetime.date:
        year = kanjidate.gengou_to_seireki(self.gengou, int(self.nen))
        return datetime.date(year, int(self.month), int(self.day))


class SexInputValue:
    def __init__(self):
        self.value = None

    def as_ident(self):
        if self.value == "男":
            return "M"
        elif self.value == "女":
            return "F"


class PatientFormValues:
    def __init__(self):
        self.patient_id = None
        self.last_name = None
        self.first_name = None
        self.last_name_yomi = None
        self.first_name_yomi = None
        self.birthday = DateInputFormValues()
        self.sex = SexInputValue()
        self.address = None
        self.phone = None

    @staticmethod
    def get(cont: Controller, win: str, exclude_patient_id=False):
        values = PatientFormValues()
        if not exclude_patient_id:
            values.patient_id = cont.get_text(win + "/PatientIdLabel")
        values.last_name = cont.get_text(win + "/LastNameInput")
        values.first_name = cont.get_text(win + "/FirstNameInput")
        values.last_name_yomi = cont.get_text(win + "/LastNameYomiInput")
        values.first_name_yomi = cont.get_text(win + "/FirstNameYomiInput")
        values.birthday.gengou = cont.get_text(win + "/Birthday/Gengou")
        values.birthday.nen = cont.get_text(win + "/Birthday/Nen")
        values.birthday.month = cont.get_text(win + "/Birthday/Month")
        values.birthday.day = cont.get_text(win + "/Birthday/Day")
        values.sex.value = cont.get_text(win + "/Sex")
        values.address = cont.get_text(win + "/AddressInput")
        values.phone = cont.get_text(win + "/PhoneInput")
        return values

    def as_model(self) -> Patient:
        p = Patient()
        if self.patient_id:
            p.patient_id = int(self.patient_id)
        p.last_name = self.last_name
        p.first_name = self.first_name
        p.last_name_yomi = self.last_name_yomi
        p.first_name_yomi = self.first_name_yomi
        p.birthday = self.birthday.as_date()
        p.sex = self.sex.as_ident()
        p.address = self.address
        p.phone = self.phone
        return p


class NewPatientWindow:
    def __init__(self, cont: Controller):
        self.cont = cont

    def set_patient(self, patient: Patient):
        birthday = sqldate_to_date(patient.birthday)
        (g, n) = kanjidate.date_to_gengou(birthday)
        self.cont.set_text("EnterPatientStage/LastNameInput", patient.last_name)
        self.cont.set_text("EnterPatientStage/FirstNameInput", patient.first_name)
        self.cont.set_text("EnterPatientStage/LastNameYomiInput", patient.last_name_yomi)
        self.cont.set_text("EnterPatientStage/FirstNameYomiInput", patient.first_name_yomi)
        self.cont.set_text("EnterPatientStage/Birthday/Gengou", g.kanji)
        self.cont.set_text("EnterPatientStage/Birthday/Nen", n)
        self.cont.set_text("EnterPatientStage/Birthday/Month", birthday.month)
        self.cont.set_text("EnterPatientStage/Birthday/Day", birthday.day)
        self.cont.set_text("EnterPatientStage/Sex", sex_to_kanji(patient.sex))
        self.cont.set_text("EnterPatientStage/AddressInput", patient.address)
        self.cont.set_text("EnterPatientStage/PhoneInput", patient.phone)

    def cancel(self):
        self.cont.click("EnterPatientStage/CancelButton")
        self.cont.wait_for_window_closed("EnterPatientStage")

    def enter(self):
        self.cont.click("EnterPatientStage/EnterButton")
        self.cont.wait_for_window_closed("EnterPatientStage")


class PatientWithHokenWindow:
    def __init__(self, cont: Controller):
        self.cont = cont

    def click_edit_button(self):
        self.cont.click("PatientWithHokenStage/EditPatientButton")

    def close(self):
        self.cont.click("PatientWithHokenStage/CloseButton")
        self.cont.wait_for_window_closed("PatientWithHokenStage")


class EditPatientWindow:
    def __init__(self, cont: Controller):
        self.cont = cont

    def get_patient_id(self):
        return self.cont.get_text("EditPatientStage/PatientIdLabel")

    def get_last_name(self):
        return self.cont.get_text("EditPatientStage/LastNameInput")

    def get_form_values(self):
        values = PatientFormValues()
        values.patient_id = self.get_patient_id()


def test_cancel_enter_patient(rc: ReceptionController):
    win = rc.open_new_patient_window()
    win.cancel()


def test_enter_patient(rc: ReceptionController, ploglistener: Listener):
    patient = Patient(
        last_name="診療",
        first_name="太郎",
        last_name_yomi="しんりょう",
        first_name_yomi="たろう",
        birthday="1959-07-18",
        sex="M",
        address="東京",
        phone="03-1234-5678",
    )
    win = rc.open_new_patient_window()
    win.set_patient(patient)
    win.enter()

    def test(msg):
        plog, body = msg
        if plog.kind == "patient-created":
            patient.patient_id = body.created.patient_id
            return patient.to_dict() == body.created.to_dict()
        else:
            return False
    ploglistener.pop_test(test)
    rc.wait_for_window_created("PatientWithHokenStage")
    edit_win = PatientWithHokenWindow(rc)
    edit_win.click_edit_button()
    rc.wait_for_window_created("EditPatientStage")
    pedit_win = EditPatientWindow(rc)
    form_values = PatientFormValues.get(rc, "EditPatientStage")
    assert patient.to_dict() == form_values.as_model().to_dict(), "Inconsistent form values in EditPatientStage"


def test_reception(rec: ReceptionController, plog: Listener):
    test_cancel_enter_patient(rec)
    test_enter_patient(rec, plog)


if __name__ == "__main__":
    cf = ControllerFactory("http://127.0.0.1:28080")
    rec = cf.create_reception_controller()
    practice_log_listener = cf.create_practice_log_listener()
    test_enter_patient(rec, practice_log_listener)


