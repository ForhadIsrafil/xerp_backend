from django.http import Http404


def get_object_or_404(model, look_up_for):
    # catch invalid uuids
    try:
        return model.objects.get(pk=look_up_for)
    except:
        raise Http404
