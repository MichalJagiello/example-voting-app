/**
 * Created by michalj on 16.02.17.
 */

var update_view = function(option_a, option_b, total) {
  var bg1 = document.getElementById('background-stats-1');
  var bg2 = document.getElementById('background-stats-2');
  var total_res = document.getElementById('total_result');

  bg1.style.width = option_a + "%";
  bg2.style.width = option_b + "%";

  $("#option_a_res").text(option_a + "%");
  $("#option_b_res").text(option_b + "%");

  if (total == 0) {
    $("#total_result").text("No votes yet");
  }
  else if (total == 1) {
    $("#total_result").text("1 vote");
  }
  else {
    $("#total_result").text(total + " votes");
  }
}

document.addEventListener("DOMContentLoaded", function(event) {
    document.body.style.opacity=1;

    setInterval(function(){
      $.get('/poll/', function(data) {
        update_view(data['option_a_res'], data['option_b_res'], Number(data['total']));
      })
    }, 500);
});
