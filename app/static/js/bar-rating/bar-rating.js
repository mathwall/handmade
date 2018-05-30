$(function() {
    let $divs = $('.custom-bar-rating');

    for(let i = 0; i < $divs.length; i++) {
        let $this = $($divs[i]);
        let $bar = $this.find('.br-select');
        let $reviewSpan = $this.find('.nb-review');
        let initialRating = $bar.attr('data-rate-initial');
        initialRating = initialRating ? initialRating : "null";
        console.log("initial", initialRating);
        console.log(typeof initialRating);
        let type = $bar.attr('data-rate-type');
        let id = $bar.attr('data-type-id');

        $bar.barrating({
            theme: 'bootstrap-stars',
            initialRating: initialRating,
            silent: true,
            onSelect: function(value, text, event) {
                if (typeof(event) !== 'undefined') {
                    // rating was selected by a user
                    let $parent = $(event.target).parent();
                    let rate = event.target.getAttribute('data-rating-value');
                    $parent.addClass('br-already-selected');
                    $.ajax({
                        url: '/api/rates/' + type,
                        data: {id: id, rate: rate },
                        dataType: 'json',
                        success: function (data) {
                            setTimeout(() => {
                                $parent.removeClass('br-already-selected');
                                $bar.barrating('set', data.new_avg);
                            }, 1000);
                            // $bar.barrating('readonly', true);
                            console.log(data);
                            console.log($reviewSpan);
                            
                            $reviewSpan.text(data.nb_review);
                        },
                        error: function(error) {
                            console.log(error.responseJSON.message);
                            $parent.addClass('br-error');
                            $parent.removeClass('br-already-selected');
                            setTimeout(() => {
                                $parent.removeClass('br-error');
                                $bar.barrating('set', initialRating);
                            }, 1000);
                            // $bar.barrating('readonly', true);
                        }
                    });
                } else {
                    // rating was selected programmatically
                    // by calling `set` method
                }
            }
        });
    }
});

