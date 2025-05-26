from secure_dispatcher import load_token, save_token # type: ignore

#Example usage
admin_token="Tech123"
save_token(admin_token) #save encrypted

loaded_token=load_token()
print("Decrypted Token".loaded_token)                        
