from django.http import JsonResponse
from django.contrib.auth.decorators import login_required , user_passes_test
from instructor.models import Section
from student.models import Comment, Reply



@login_required
def add_comment(request, id):
    current_section = Section.objects.get(id=id)
    if request.method == "POST":
        comment = request.POST.get('comment')
        new_comment = Comment(person=request.user, section=current_section, content=comment)
        new_comment.save()
        return JsonResponse({"comment": new_comment.content})
    
@login_required
def add_reply(request, id):
    comment_to_replay = Comment.objects.get(id=id)
    if request.method == "POST":
        reply = request.POST.get('reply')
        new_reply = Reply(comment = comment_to_replay, person = request.user, content = reply)
        new_reply.save()
        return JsonResponse({"reply": new_reply.content})
    

@login_required
def view_replies(request, id):
    comment = Comment.objects.get(id=id)
    all_replies = Reply.objects.filter(comment=comment)
    all_data = []
    for i in all_replies:
        data = {
            i.person.username : i.content
        }
        all_data.append(data)
    return JsonResponse({'replies':all_data})