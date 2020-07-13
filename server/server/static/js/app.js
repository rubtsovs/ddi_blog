$(() => {
  const AddComment = () => {
    let comment = $("#comment").val();
    let parent = $("#contactparent").val();
    console.log(comment, parent);
    $.ajax({
      type: "POST",
      dataType: "json",
      url: window.location.pathname,
      data: {
        comment: comment,
        parent: parent,
      },
      beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
      },
    });
  };
  $("#comment-form").on("submit", AddComment);
  var infinite = new Waypoint.Infinite({
    element: $(".infinite-container")[0],
    onBeforePageLoad: function () {
      $(".loading").show();
    },
    onAfterPageLoad: function ($items) {
      $(".loading").hide();
    },
  });
});
function addReview(name, id) {
  document.getElementById("contactparent").value = id;
  document.getElementById("comment").innerText = `${name}, `;
}
