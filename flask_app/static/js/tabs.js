const ACTIVE_CLASS = 'is-active';

$("[tab-target]").on("click", function (e) {
    let selected = this.getAttribute('tab-target');
    $(this).siblings().removeClass(ACTIVE_CLASS);
    $(this).addClass(ACTIVE_CLASS);
    $("[tab-content]").removeClass(ACTIVE_CLASS)
    $("[tab-content=" + selected + "]").addClass(ACTIVE_CLASS)
});