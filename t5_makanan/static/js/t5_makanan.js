var field = 1;
$("#id_h").change(function () {
  var id = $("#id_h").val();
  if (id != "-- pilih id --") {
    $.ajax({
      url: "/makanan/tr-makan/getKode/" + id,
      success: function (hasil) {
        var kodeHotel = hasil.kodehotel;
        $("#kodeHotel").val(kodeHotel);
        $(".kodePaket").empty();
        $(".kodePaket").append('<option value="">-- pilih paket --</option>');
        $.each(hasil.kodepaket, function (index, value) {
          $(".kodePaket").append(
            '<option value="' + value + '">' + value + "</option>"
          );
        });
      },
    });
  }
});

$("#tambah").click(function () {
  var isi = $.trim($("#paket1").html());
  field = field + 1;
  $("#blockPaket").append(
    '<tr><td><label for="paket' +
      field +
      '"><b>Kode Paket: </b></label></td><td><select name="paket' +
      field +
      '" class="kodePaket" id="paket' +
      field +
      '" required oninvalid="alert(\'Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu!!!\');">' +
      isi +
      '</select><a class="hapus" id="cross' +
      field +
      '">❌</a></td></tr>'
  );
});

$(document).on("click", ".hapus", function () {
  $(this).parent().parent().remove();
});
