import torch, numpy, cv2

hair_list=['blonde hair', 'purple hair', 'red hair', 'blue hair', 'pink hair','green hair',
           'white hair', 'gray hair', 'black hair', 'brown hair', 'aqua hair', 'orange hair']

eyes_list=['pink eyes', 'purple eyes', 'aqua eyes', 'black eyes', 'blue eyes', 'yellow eyes',
           'green eyes', 'orange eyes', 'red eyes', 'brown eyes', 'gray eyes']

def load_model(device):
    model_dir = 'model'

    model_path = f'{model_dir}/G1_torchscript_cpu.pt'
    #device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torch.jit.load(model_path, map_location=device)
    for parameter in model.parameters(): 
        parameter.requires_grad = False
    return model.eval()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
modelG = load_model(device)
z_dim = 200

def create_tag(hair_color, eyes_color):
    hair_color = hair_color +' hair'
    eyes_color = eyes_color +' eyes'
    for i, color in enumerate(hair_list):
        if color in hair_color:
            hair_tag = torch.zeros(len(hair_list))
            hair_tag[i] = 1.0
    for i, color in enumerate(eyes_list):
        if color in eyes_color:
            eyes_tag = torch.zeros(len(eyes_list))
            eyes_tag[i] = 1.0

    return hair_tag.to(device), eyes_tag.to(device)

def image_gan(hair_color, eyes_color):

    hair_tag, eyes_tag = create_tag(hair_color, eyes_color)
    z = torch.randn(z_dim).to(device)
    hair_tag=hair_tag.unsqueeze(0)
    eyes_tag=eyes_tag.unsqueeze(0)
    z=z.unsqueeze(0)

    predict_img = (modelG(z, hair_tag, eyes_tag)+1)/2
    predict_img = predict_img.to(torch.device('cpu'))[0]
    predict_img = numpy.array(predict_img.permute(1,2,0))
    #predict_img = cv2.resize(predict_img, (320,320), interpolation=cv2.INTER_LINEAR)

    #return {'class': prediction, 'probability': probability}
    return numpy.uint8(predict_img*255)
    #return predict_img