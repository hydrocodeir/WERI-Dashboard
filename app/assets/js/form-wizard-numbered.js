/**
 *  Form Wizard
 */

"use strict";

$(function () {
  const select2 = $(".select2"),
    selectPicker = $(".selectpicker");

  // Bootstrap select
  if (selectPicker.length) {
    selectPicker.selectpicker();
  }

  // select2
  if (select2.length) {
    select2.each(function () {
      var $this = $(this);
      $this.wrap('<div class="position-relative"></div>');
      $this.select2({
        placeholder: "Select value",
        dropdownParent: $this.parent(),
      });
    });
  }
});

(function () {
  // Numbered Wizard
  // --------------------------------------------------------------------
  const wizardNumbered = document.querySelector(".wizard-numbered"),
    wizardNumberedBtnNextList = [].slice.call(
      wizardNumbered.querySelectorAll(".btn-next")
    ),
    wizardNumberedBtnPrevList = [].slice.call(
      wizardNumbered.querySelectorAll(".btn-prev")
    ),
    wizardNumberedBtnSubmit = wizardNumbered.querySelector(".btn-submit");

  if (typeof wizardNumbered !== undefined && wizardNumbered !== null) {
    const numberedStepper = new Stepper(wizardNumbered, {
      linear: false,
    });
    if (wizardNumberedBtnNextList) {
      wizardNumberedBtnNextList.forEach((wizardNumberedBtnNext) => {
        wizardNumberedBtnNext.addEventListener("click", (event) => {
          numberedStepper.next();
        });
      });
    }
    if (wizardNumberedBtnPrevList) {
      wizardNumberedBtnPrevList.forEach((wizardNumberedBtnPrev) => {
        wizardNumberedBtnPrev.addEventListener("click", (event) => {
          numberedStepper.previous();
        });
      });
    }
  }
})();

(function () {
  // Numbered Wizard
  // --------------------------------------------------------------------
  const wizardNumberedEmp = document.querySelector(".wizard-numbered-emp"),
    wizardNumberedEmpBtnNextList = [].slice.call(
      wizardNumberedEmp.querySelectorAll(".btn-next-emp")
    ),
    wizardNumberedEmpBtnPrevList = [].slice.call(
      wizardNumberedEmp.querySelectorAll(".btn-prev-emp")
    ),
    wizardNumberedEmpBtnSubmit = wizardNumberedEmp.querySelector(".btn-submit-emp");

  if (typeof wizardNumberedEmp !== undefined && wizardNumberedEmp !== null) {
    const numberedStepperEmp = new Stepper(wizardNumberedEmp, {
      linear: false,
    });
    if (wizardNumberedEmpBtnNextList) {
      wizardNumberedEmpBtnNextList.forEach((wizardNumberedEmpBtnNext) => {
        wizardNumberedEmpBtnNext.addEventListener("click", (event) => {
          numberedStepperEmp.next();
        });
      });
    }
    if (wizardNumberedEmpBtnPrevList) {
      wizardNumberedEmpBtnPrevList.forEach((wizardNumberedEmpBtnPrev) => {
        wizardNumberedEmpBtnPrev.addEventListener("click", (event) => {
          numberedStepperEmp.previous();
        });
      });
    }
  }
})();

(function () {
  // Numbered Wizard
  // --------------------------------------------------------------------
  const wizardNumberedEar = document.querySelector(".wizard-numbered-ear"),
    wizardNumberedEarBtnNextList = [].slice.call(
      wizardNumberedEar.querySelectorAll(".btn-next-ear")
    ),
    wizardNumberedEarBtnPrevList = [].slice.call(
      wizardNumberedEar.querySelectorAll(".btn-prev-ear")
    ),
    wizardNumberedEarBtnSubmit = wizardNumberedEar.querySelector(".btn-submit-ear");

  if (typeof wizardNumberedEar !== undefined && wizardNumberedEar !== null) {
    const numberedStepperEar = new Stepper(wizardNumberedEar, {
      linear: false,
    });
    if (wizardNumberedEarBtnNextList) {
      wizardNumberedEarBtnNextList.forEach((wizardNumberedEarBtnNext) => {
        wizardNumberedEarBtnNext.addEventListener("click", (event) => {
          numberedStepperEar.next();
        });
      });
    }
    if (wizardNumberedEarBtnPrevList) {
      wizardNumberedEarBtnPrevList.forEach((wizardNumberedEarBtnPrev) => {
        wizardNumberedEarBtnPrev.addEventListener("click", (event) => {
          numberedStepperEar.previous();
        });
      });
    }
  }
})();

(function () {
  // Numbered Wizard
  // --------------------------------------------------------------------
  const wizardNumberedEp = document.querySelector(".wizard-numbered-ep"),
    wizardNumberedEpBtnNextList = [].slice.call(
      wizardNumberedEp.querySelectorAll(".btn-next-ep")
    ),
    wizardNumberedEpBtnPrevList = [].slice.call(
      wizardNumberedEp.querySelectorAll(".btn-prev-ep")
    ),
    wizardNumberedEpBtnSubmit = wizardNumberedEp.querySelector(".btn-submit-ep");

  if (typeof wizardNumberedEp !== undefined && wizardNumberedEp !== null) {
    const numberedStepperEp = new Stepper(wizardNumberedEp, {
      linear: false,
    });
    if (wizardNumberedEpBtnNextList) {
      wizardNumberedEpBtnNextList.forEach((wizardNumberedEpBtnNext) => {
        wizardNumberedEpBtnNext.addEventListener("click", (event) => {
          numberedStepperEp.next();
        });
      });
    }
    if (wizardNumberedEpBtnPrevList) {
      wizardNumberedEpBtnPrevList.forEach((wizardNumberedEpBtnPrev) => {
        wizardNumberedEpBtnPrev.addEventListener("click", (event) => {
          numberedStepperEp.previous();
        });
      });
    }
  }
})();

(function () {
  // Numbered Wizard
  // --------------------------------------------------------------------
  const wizardNumberedE2P = document.querySelector(".wizard-numbered-e2p"),
    wizardNumberedE2PBtnNextList = [].slice.call(
      wizardNumberedE2P.querySelectorAll(".btn-next-e2p")
    ),
    wizardNumberedE2PBtnPrevList = [].slice.call(
      wizardNumberedE2P.querySelectorAll(".btn-prev-e2p")
    ),
    wizardNumberedE2PBtnSubmit = wizardNumberedE2P.querySelector(".btn-submit-e2p");

  if (typeof wizardNumberedE2P !== undefined && wizardNumberedE2P !== null) {
    const numberedStepperE2P = new Stepper(wizardNumberedE2P, {
      linear: false,
    });
    if (wizardNumberedE2PBtnNextList) {
      wizardNumberedE2PBtnNextList.forEach((wizardNumberedE2PBtnNext) => {
        wizardNumberedE2PBtnNext.addEventListener("click", (event) => {
          numberedStepperE2P.next();
        });
      });
    }
    if (wizardNumberedE2PBtnPrevList) {
      wizardNumberedE2PBtnPrevList.forEach((wizardNumberedE2PBtnPrev) => {
        wizardNumberedE2PBtnPrev.addEventListener("click", (event) => {
          numberedStepperE2P.previous();
        });
      });
    }
  }
})();

(function () {
  // Numbered Wizard
  // --------------------------------------------------------------------
  const wizardNumbereduref = document.querySelector(".wizard-numbered-uref"),
    wizardNumberedurefBtnNextList = [].slice.call(
      wizardNumbereduref.querySelectorAll(".btn-next-uref")
    ),
    wizardNumberedurefBtnPrevList = [].slice.call(
      wizardNumbereduref.querySelectorAll(".btn-prev-uref")
    ),
    wizardNumberedurefBtnSubmit = wizardNumbereduref.querySelector(".btn-submit-uref");

  if (typeof wizardNumbereduref !== undefined && wizardNumbereduref !== null) {
    const numberedStepperuref = new Stepper(wizardNumbereduref, {
      linear: false,
    });
    if (wizardNumberedurefBtnNextList) {
      wizardNumberedurefBtnNextList.forEach((wizardNumberedurefBtnNext) => {
        wizardNumberedurefBtnNext.addEventListener("click", (event) => {
          numberedStepperuref.next();
        });
      });
    }
    if (wizardNumberedurefBtnPrevList) {
      wizardNumberedurefBtnPrevList.forEach((wizardNumberedurefBtnPrev) => {
        wizardNumberedurefBtnPrev.addEventListener("click", (event) => {
          numberedStepperuref.previous();
        });
      });
    }
  }
})();

(function () {
  // Numbered Wizard
  // --------------------------------------------------------------------
  const wizardNumberedTime= document.querySelector(".wizard-numbered-timeline"),
    wizardNumberedTimeBtnNextList = [].slice.call(
      wizardNumberedTime.querySelectorAll(".btn-next-timeline")
    ),
    wizardNumberedTimeBtnPrevList = [].slice.call(
      wizardNumberedTime.querySelectorAll(".btn-prev-timeline")
    ),
    wizardNumberedTimeBtnSubmit = wizardNumberedTime.querySelector(".btn-submit-timeline");

  if (typeof wizardNumberedTime!== undefined && wizardNumberedTime!== null) {
    const numberedStepperTime= new Stepper(wizardNumberedTime, {
      linear: false,
    });
    if (wizardNumberedTimeBtnNextList) {
      wizardNumberedTimeBtnNextList.forEach((wizardNumberedTimeBtnNext) => {
        wizardNumberedTimeBtnNext.addEventListener("click", (event) => {
          numberedStepperTime.next();
        });
      });
    }
    if (wizardNumberedTimeBtnPrevList) {
      wizardNumberedTimeBtnPrevList.forEach((wizardNumberedTimeBtnPrev) => {
        wizardNumberedTimeBtnPrev.addEventListener("click", (event) => {
          numberedStepperTime.previous();
        });
      });
    }
  }
})();
