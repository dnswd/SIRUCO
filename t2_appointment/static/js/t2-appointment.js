$(document).ready(function () {

    console.log('ready');
    $('#button-submit-cek').click(function (e) {
        // formnya disubmit
        var cek_text = $('#cek-isi-form').val();
        var cek_text2 = $('#cek-isi-form2').val();
        var selected = $('#opsi-dropdown').find(":selected").val();
        var selected2 = $('#opsi-dropdown2').find(":selected").val();
        if (selected == '' || selected2 == '' || cek_text == '' || cek_text2 == '') {
            e.preventDefault();
            input_kosong();
        }
    })

    function input_kosong() {
        $('#input-kosong').empty();
        $('#input-kosong').append('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu');
    }

    $('.opsi-rs').change(function () {
        var selected = $(this).find(":selected").val();
        if (selected != '') {
            $.ajax({
                url: '/appointment/get-next-ruang/' + selected,
                type: 'GET',
                datatype: 'JSON',
                success: function (data) {
                    $('#no-ruang').val(data.kodeRuangan);
                },
                error: function () {
                    alert("error");
                }
            })
        }
    })

    $('.opsi-rs2').change(function () {
        var selected = $(this).find(":selected").val();
        if (selected != '') {
            $.ajax({
                url: '/appointment/get-ruang-rs/' + selected,
                type: 'GET',
                datatype: 'JSON',
                success: function (data) {
                    var items = data.list_kodeRuangan;
                    console.log(items);
                    for (var i = 0; i < items.length; i++) {
                        console.log(items[i].kodeRuangan);
                        $('.opsi-ruangan').append('<option value="' + items[i].kodeRuangan + '">' + items[i].kodeRuangan + '</option>');
                    }
                },
                error: function () {
                    alert("error");
                }
            })
        }
    })

    $('.opsi-ruangan').change(function () {
        var kodeRS = $('.opsi-rs2').find(":selected").val();
        var kodeRuangan = $(this).find(":selected").val();
        console.log(kodeRS);
        console.log(kodeRuangan);
        if (kodeRS != '' && kodeRuangan != '') {
            $.ajax({
                url: '/appointment/get-next-bed/' + kodeRS + '/' + kodeRuangan,
                type: 'GET',
                datatype: 'JSON',
                success: function (data) {
                    $('#no-bed').val(data.kodeBed);
                },
                error: function () {
                    alert("error");
                }
            })
        }
    })

});