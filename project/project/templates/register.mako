<%inherit file="default.mako" />
<%block name="title">Zaregistrujte sa!</%block>
<%block name="page_content">
<h2>Zaregistrujte sa!</h2>
<%def name="error(field)">
% if field in errors:
    <span class='error'>${error_messages[errors[field]]}</span>
% endif
</%def>
<form method="POST">
    <div class="input-group">
        <label for="email">E-mail</label>
        <input type="email" name="email" id="email" required/>
        ${error('email')}
    </div>
    <div class="input-group">
        <label for="password">Heslo</label>
        <input type="password" name="password" id="password" required/>
        ${error('password')}
    </div>
    <div class="input-group">
        <label for="password_repeat">Heslo znovu</label>
        <input type="password" name="password_repeat" id="password_repeat" required/>
    </div>
    <div class="input-group trigger">
        <label for="role">Sa cítiš, že si interpret?</label>
        <input type="checkbox" name="role" id="role"/>
    </div>
    <div class="input-group default_hide">
        <label for="interpret_name">Ako ťa ľudia oslovujú?</label>
        <input type="text" name="interpret_name" id="interpret_name"/>
    </div>
    <button type="submit" class="submit-form">Zaregistrovať sa</button>
</form>
</%block>
