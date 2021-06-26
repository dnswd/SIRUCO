$("#id_kode_hotel").on("change", (e) => {
  loadOptions(e.target.value);
});

function loadOptions(kodehotel) {
  $("#id_kode_ruangan").prop("disabled", true);
  $("#submit").prop("disabled", true);
  $.ajax({
    type: "GET",
    url: `/hotel/rsvp/api/${kodehotel}`,
    success: (data) => {
      $("#id_kode_ruangan")[0].innerHTML = "";
      data = JSON.parse(data);
      data.forEach((kode) => {
        $("#id_kode_ruangan").append(new Option(kode, kode));
      });
      $("#id_kode_ruangan").prop("disabled", false);
      $("#submit").prop("disabled", false);
    },
  });
}

loadOptions($("#id_kode_hotel")[0].value);
