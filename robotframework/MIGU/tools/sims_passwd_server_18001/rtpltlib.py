import com.aspire.sims.rtplt.component.security.util.PasswordUtil as PasswordUtil

def encryptpasswd(staff_id, password):
    result = PasswordUtil.cryptPassword(str(staff_id),str(password))
    return result